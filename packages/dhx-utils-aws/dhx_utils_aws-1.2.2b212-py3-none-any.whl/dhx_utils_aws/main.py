"""
Copyright (c) 2021 RoZetta Technology Pty Ltd. All rights reserved.
"""
import argparse
import sys
from typing import Callable, Any
import pkg_resources  # part of setuptools
import simplejson as json
from dhx_utils.errors import ParamError, DataHexError
from dhx_utils.logger import get_logger
import dhx_utils_aws.ingestion
from dhx_utils_aws.ingestion import ProcessingJobStatus, ProcessingJobError
import dhx_utils_aws.s3
from dhx_utils_aws.events import send_event_to_bus, EventBusClient, DataHexEventBusClient


SUCCESS = 0
FAILURE = 1


def get_version():
    """
    :return: The version of the tool
    """
    return pkg_resources.require("dhx-utils-aws")[0].version


def send_event(args):
    """ Send an event to an event bus. """
    if not args.source:
        raise ParamError("'source' is required for this command")
    if not args.detail_type:
        raise ParamError("'detail-type' is required for this command")
    if not args.detail and not args.detail_file:
        raise ParamError("You must specify at least the detail or the file to load the detail from.")
    if args.detail_file:
        # Load the detail from a file.
        with open(args.detail_file, encoding='utf-8') as input_file:
            detail = json.load(input_file)
    else:
        # Load the detail from the arg.
        detail = json.loads(args.detail)
    send_event_to_bus(args.bus_name, args.source, args.detail_type, detail)


def load_params_file(args):
    """ Loads params from a file """
    content = dhx_utils_aws.ingestion.load_params_file(args.params_file_path)
    print(json.dumps(content, indent=2))


def send_data_staged(args):
    """ Send a DataAssetStaged event to the DataHex bus """
    if not args.assets_file_path:
        raise ParamError("Assets file path is required for this command")

    source = args.source or "datahex.dhx_utils_aws"

    with open(args.assets_file_path, "r", encoding="utf-8") as stream:
        content = json.load(stream)

        if args.bus_name:
            # Use custom bus name.
            bus_client = EventBusClient(event_bus_name=args.bus_name, source=source)
        else:
            # Use bus name based on environment variables.
            bus_client = DataHexEventBusClient(source=source)
        DataHexEventBusClient.set_default_event_client(bus_client)
        dhx_utils_aws.ingestion.send_data_staged_events(content)


def read_s3_object(args):
    """ Reads an s3 JSON object """
    if not args.s3_file_path:
        raise ParamError("S3 file path is required for this command")
    content = dhx_utils_aws.s3.read_s3_json_object(args.s3_file_path)
    print(json.dumps(content, indent=2))


def async_job_completed(args):
    """callback function to send async task completion notice"""
    status = ProcessingJobStatus(args.status) if args.status else None
    job_error = ProcessingJobError(args.error) if args.error else None
    output = json.loads(args.output) if args.output else None

    dhx_utils_aws.ingestion.async_job_completed(task_token=args.task_token,
                                                status=status,
                                                output=output,
                                                job_error=job_error,
                                                cause=args.cause)


def main():
    """ Main entry to the CLI tool """

    parser = argparse.ArgumentParser(description="RoZetta DataHex Utility for AWS")
    parser.add_argument("-V", "--version", action="version", version=get_version())
    sub_parsers = parser.add_subparsers(dest="command")
    command_mappings = {}

    def add_sub_parser(command: str, help_doc: str, command_func: Callable[[Any], Any]) -> argparse.ArgumentParser:
        """ Help function to add a sub parser """
        cmd_parser = sub_parsers.add_parser(command, help=help_doc)
        command_mappings[command] = command_func
        return cmd_parser

    # Load params file command
    sub_parser = add_sub_parser("load-params-file", "Load a params file from a given path", load_params_file)
    sub_parser.add_argument("--params-file-path", help="The path to the parameters file.")

    # Read S3 JSON command
    sub_parser = add_sub_parser("read-s3-json", "Reads a JSON file from an S3 path", read_s3_object)
    sub_parser.add_argument("--s3-file-path", required=True, help="The path to an s3 object.")

    # Send event command
    sub_parser = add_sub_parser("send-event", "Send an event to an AWS EventBridge Event Bus", send_event)
    sub_parser.add_argument("--bus-name", "-b", required=True, help="Full name of the bus")
    sub_parser.add_argument("--source", "-s", required=True, help="Source of the eventbridge event")
    sub_parser.add_argument("--detail-type", "-t", required=True, help="The detail type of the eventbridge event.")
    sub_parser.add_argument("--detail", "-d", help="The detail payload (JSON string)")
    sub_parser.add_argument("--detail-file", "-f", help="The file containing the detail payload")

    # Send data staged event
    sub_parser = add_sub_parser("send-data-staged", "Send DataAssetStaged event to DataHex Event Bus",
                                send_data_staged)
    sub_parser.add_argument("--assets-file-path", required=True, help="The path to the assets file.")
    sub_parser.add_argument("--source", "-s", help="Source of the eventbridge event")
    sub_parser.add_argument("--bus-name", "-b", help="Full name of the bus")

    # Flag that an async processing job has completed by doing a callback to a state machine.
    sub_parser = add_sub_parser("async-job-completed",
                                "Notify the ingestion state machine that an async processing job has completed",
                                async_job_completed)
    sub_parser.add_argument("--status", "-s",
                            choices=[st.value for st in list(ProcessingJobStatus)],
                            help="Status of the completed job")
    sub_parser.add_argument("--task-token", "-t",
                            help="Task token to send the async callback with. If not provided, it will take it from "
                                 "the environment variable TASK_TOKEN")
    sub_parser.add_argument("--output", "-o",
                            help="JSON payload for the output of the async task when a job ran successfully")
    sub_parser.add_argument("--error", "-e",
                            choices=[err.value for err in list(ProcessingJobError)],
                            help="Error code if the job failed.")
    sub_parser.add_argument("--cause", "-c",
                            help="Additional information about the cause of the error")

    # Parse the command argument and based on the command, call the function that is mapped to that command.
    logger = get_logger("main")
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return FAILURE

    try:
        func = command_mappings.get(args.command)
        if not func:
            raise ParamError(f"Unknown command '{args.command}'")
        func(args)
        return SUCCESS

    except DataHexError as e:
        logger.error(str(e))
        return FAILURE


if __name__ == '__main__':  # pragma: no coverage
    sys.exit(main())
