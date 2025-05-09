"""
Copyright (c) 2021 RoZetta Technology Pty Ltd. All rights reserved.
"""
import os

from typing import Dict
from enum import Enum
import simplejson as json
import boto3
from botocore.exceptions import ClientError
from dhx_utils.errors import APIError, ParamError, ServerError
from dhx_utils.logger import get_logger
from dhx_utils_aws.s3 import read_s3_json_object
from dhx_utils_aws.events import put_datahex_event


logger = get_logger()


def send_data_staged_events(payload: Dict) -> None:
    """ Bulk send out 'DataAssetStaged' events for a list of data assets for a given period and
    partition. The payload parameter should comply to the following format:
    {
        "period": "2021-08",   ## the period that is being staged
        "partition": {},       ## the partition that is being staged
        "data_assets":         ## the list of data assets being staged
        [
            {
                "data_asset_id": "xxxx-xxxx-1111",                    ## the data asset ID that was staged
                "data_location": "s3://bucket/path/path/YYYY/MM/"     ## the data location of the sub data
            },
            {
                "data_asset_id": "xxxx-xxxx-2222",
                "data_location": "s3://bucket/path/path/YYYY/MM/"
            },
            ...
        ]
    }

    The data staged events will be send to the DataHex Event Bus, with the following payload:
    {
        "data_asset_id": ${asset_id},
        "period": ${period},
        "partition": ${partition},  # optional
        "supplement":
        {
            "data_location": ${data_location}
        }
    }

    :param payload: The payload parameters of the format described above.
    :return: None
    """
    period = payload.get('period')
    data_assets = payload.get('data_assets')
    if not period:
        raise APIError("Unable to send DataAssetStaged event without a period.")
    if data_assets is None:
        raise APIError("Unable to send DataAssetStaged event without a list of data assets.")
    if len(data_assets) == 0:
        logger.warning("No DataAssetStaged event sent as the data asset list is empty.")
        return

    # Do a quick validation that mandatory fields are there before sending out the events.
    fields = ['data_asset_id', 'data_location']
    for item in data_assets:
        for prop in fields:
            if prop not in item:
                raise APIError(
                    "Abort sending DataAssetStaged events as one of the data assets"
                    f" is missing the mandatory fields: { ','.join(fields) }")

    # Note: partition is option as not all data assets have it.
    partition = payload.get('partition')
    for item in data_assets:
        details = {
            "data_asset_id": item.get('data_asset_id'),
            "period": period,
            "supplement":
            {
                "data_location": item.get('data_location'),
            },
        }
        if partition:
            # Add the partition info if it exists for this data asset.
            details.update(partition=partition)

        put_datahex_event(detail_type='DataAssetStaged', detail=details)


def load_params_file(params_file_path: str = None) -> Dict:
    """ Load a parameters file that is generally created by a DataHex generic ingestion pipeline.

    :param params_file_path:
        The S3 path where the parameters file can be found. If this is not specified, this
        function will look for it in the env variable PARAMS_FILE, and if it is not there too,
        it will throw an exception. This file is expected to be in JSON format.
    :return: The content loaded from the JSON file as a dictionary.
    """

    if not params_file_path:
        params_file_path = os.getenv('PARAMS_FILE')
    if not params_file_path:
        raise APIError("No params file specified.")

    content = read_s3_json_object(params_file_path)
    # Check that it is a params file.
    params = content.get('params')
    if not params:
        raise APIError("Invalid params file, it should contain a 'params' attribute.")
    return content


# Async Processing Job status Enum class
class ProcessingJobStatus(Enum):
    SUCCESS = 'success'
    FAILED = 'failed'


class ProcessingJobError(Enum):
    DATA_ERROR = "DataError"  # There was a data issue while running the processing job.
    PIPELINE_FAILURE = "PipelineFailure"  # The processing job encountered an unexpected error.


def async_job_completed(task_token: str = None,
                        status: ProcessingJobStatus = None,
                        output: dict = None,
                        job_error: ProcessingJobError = None,
                        cause: str = None) -> None:
    """ Carry out activities to indicate that an async processing job has finished and would like to notify
    the state machine of its outcome.

    :param task_token: A token provided by Step Function to identify the state machine that is waiting for
                       this async callback. If not provided, this function will attempt to get it from the
                       environment variable TASK_TOKEN.
    :param status: The processing job status to indicate if the job ran successfully or failed. If not
                   specified, it will default to success if no error was passed in.
    :param output: Optional task output to be passed to next state of the state machine. This is only used if
                   the job status is marked as successful.
    :param job_error: Indicate the type of error that causes this job to fail.
    :param cause: Provides a bit more information about the error.
    """
    if not status:
        status = ProcessingJobStatus.SUCCESS
    if not task_token:
        task_token = os.getenv("TASK_TOKEN")
        if not task_token:
            raise ParamError("Unable to notify async job completed without a task token.")

    if status == ProcessingJobStatus.SUCCESS and (job_error or cause):
        raise ParamError("Successful jobs should not have an error code or error cause.")
    if status == ProcessingJobStatus.FAILED and output:
        raise ParamError("Only successful jobs can have an output payload.")

    try:
        client = boto3.client('stepfunctions')
        if status == ProcessingJobStatus.SUCCESS:
            if not output:
                output = {}
            logger.info("Sending job completed with success with token %s and output %s", task_token, output)
            client.send_task_success(taskToken=task_token, output=json.dumps(output))
            logger.info("Job success status sent.")
        else:  # assume error status
            if not job_error:
                job_error = ProcessingJobError.PIPELINE_FAILURE
            logger.info("Sending job failed status with token %s, error:%s, cause:%s",
                        task_token, job_error.value, cause)
            client.send_task_failure(taskToken=task_token, error=job_error.value, cause=cause if cause else "")
            logger.info("Job failed status sent.")

    except ClientError as error:
        raise ServerError(f"Unable to send an async callback to the state machine: {str(error)}") from error
