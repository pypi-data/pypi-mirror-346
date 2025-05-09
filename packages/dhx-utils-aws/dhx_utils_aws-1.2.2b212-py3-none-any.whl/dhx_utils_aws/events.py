"""
Copyright (c) 2021 RoZetta Technology Pty Ltd. All rights reserved.

This module provides some helper functions and classes for other DataHex module
to send events onto an event bus. There are 2 simple approaches to using this module:

1.  Defining the required environment variables and calling `put_datahex_event()` function.
    This approach is good for apps like lambda functions and ECS tasks whereby environment
    variables are used for passing information.

    Environment variables are:
    EVENT_BUS_NAME="dhx-dev-DataHexEventBus"  # Normally taken from parameter store via CFN params.
    SERVICE="catalog"
    COMPONENT="backend.api"

    Note: if you do not define EVENT_BUS_NAME but the variables `PRODUCT`/`PROJECT` and `ENVIRONMENT`
    are set, then the module will attempt to derive the event bus name from these variables.

    put_datahex_event(detail_type="DataAssetStaged", detail={"data_asset_id":"1234})

2.  Explicitly passing the necessary parameters:

    client = DataHexEventBusClient(project="dhx", env="dev", service="oms", component="backend.api")
    client.put_event(detail_type="DataAssetStaged", detail={"data_asset_id": "1234-1234"})

To put events onto other event buses (not specific to DataHex), you can also create your own EventBusClient:

    client = EventBusClient(event_bus_name="dhx-dev-MyEventBus", source="datahex.oms.api")
    client.put_event(detail_type="MyEventType", detail={"key": "value1"})
    client.put_event(detail_type="MyEventType", detail={"key": "value2"})

"""

from typing import Dict
from datetime import datetime
import os
import boto3
from botocore.exceptions import ClientError
import simplejson as json
from dhx_utils.errors import APIError, ServerError


class EventBusClient:
    """ A DataHex helper class to put events onto AWS EventBridge's event bus."""

    def __init__(self, event_bus_name: str, source: str):
        """ Create a client that will only put event onto a specific event bus. Once created, the client can only
        send event to that bus, with the event source being the 'source' specified during init.

        :param event_bus_name: the full event bus name e.g. "dhx-dev-DataEventBus"
        :param source: the full component name e.g. "datahex.dpu.api.upload"
        """
        self._events_client = None
        self._event_bus_name = event_bus_name
        self._source = source

    @property
    def events_client(self):
        if not self._events_client:
            self._events_client = boto3.client('events')
        return self._events_client

    def put_event(self, detail_type: str, detail: dict) -> None:
        """ Put an event on the event bus.

        :param detail_type: The 'detail-type' field of the event to put.
        :param detail: The 'detail' payload of the event to put.
        :return: None
        """
        try:
            response = self.events_client.put_events(
                Entries=[
                    {
                        'Time': datetime.utcnow(),
                        'EventBusName': self._event_bus_name,
                        'Source': self._source,
                        'DetailType': detail_type,
                        'Detail': json.dumps(detail)
                    },
                ]
            )

            if response['FailedEntryCount'] != 0:
                raise APIError(f'Failed to put event onto the bus {self._event_bus_name}')
        except ClientError as e:
            raise APIError(f'Failed to put event onto the bus {self._event_bus_name}') from e


# An internal DataHex specific event client used for sending events to the common DataHex event bus using
# a single instance.
class DataHexEventBusClient(EventBusClient):

    DATAHEX_EVENT_BUS_NAME = "DataHexEventBus"
    SOURCE_PREFIX = "datahex"  # Prefix for all DataHex services and components when defining the event sources.

    @classmethod
    def get_datahex_event_bus_name(cls, project: str = None, product: str = None, env: str = None) -> str:
        """ Derive the name of the event bus based on either the project/product/env specified or from the
        environment variables ('EVENT_BUS_NAME', or 'PROJECT/PRODUCT/ENVIRONMENT').

        :param project: Name of the project (e.g. 'dhx')
        :param product: Name of the product (e.g. 'dhx') - use either project or product
        :param env: The env that it is running in (e.g. 'dev')
        :return: The event bus name (e.g. dhx-dev-DataHexEventBus)
        """
        event_bus_name = os.getenv("EVENT_BUS_NAME")
        if not event_bus_name:
            # Not declared in the environment variable. Try and derive it from other environment variables.
            product = project or product or os.getenv('PROJECT') or os.getenv('PRODUCT')
            env = env or os.getenv('ENVIRONMENT')
            if not product or not env:
                raise ServerError("Unable to determine the DataHex event bus name. You need to define either "
                                  "the environment variable EVENT_BUS_NAME, or defined PRODUCT/PROJECT "
                                  "and ENVIRONMENT")
            event_bus_name = f"{product}-{env}-{cls.DATAHEX_EVENT_BUS_NAME}"
        return event_bus_name

    @classmethod
    def get_event_source_name(cls, service: str = None, component: str = None) -> str:
        """ Derive the name of the event source based on either the service/component specified or from the
        environment variables ('SERVICE' & 'COMPONENT'). The 'component' part is optional but service must be
        specified or an exception will be raised.

        :param service: Name of the service that emits the event (e.g. 'oms', 'catalog')
        :param component: Name of the component & sub-components that emits the event (e.g. 'backend.api')
        :return: The name of the event source.
        """
        # Determine the event source using environment variables.
        service = service or os.getenv('SERVICE')
        component = component or os.getenv('COMPONENT')
        if not service:
            raise ServerError("Unable to determine the DataHex event source. You need to define the environment "
                              "variable SERVICE in order to put events onto DataHex event bus")
        component = f".{component}" if component else ""
        return f"{cls.SOURCE_PREFIX}.{service}{component}"  # e.g. datahex.catalog.api

    def __init__(self, **kwargs):
        """ Constructor

        :param project: Name of the project (e.g. 'dhx')
        :param product: Name of the product (e.g. 'dhx') - use either project or product
        :param env: The env that it is running in (e.g. 'dev')
        :param source: Name of the source that emits the event (e.g. 'datahex.oms.backend') - also see service
        :param service: Name of the service that emits the event (e.g. 'oms', 'catalog')
        :param component: Name of the component & sub-components that emits the event (e.g. 'backend.api')
        """
        project = kwargs.get('project')
        product = kwargs.get('product')
        env = kwargs.get('env')
        source = kwargs.get('source')
        service = kwargs.get('service')
        component = kwargs.get('component')
        super().__init__(event_bus_name=self.get_datahex_event_bus_name(project, product, env),
                         source=source or self.get_event_source_name(service, component))

    # Default DataHex event client (singleton)
    _default_event_client = None

    @classmethod
    def get_default_event_client(cls) -> EventBusClient:
        if not cls._default_event_client:
            cls._default_event_client = DataHexEventBusClient()
        return cls._default_event_client

    @classmethod
    def set_default_event_client(cls, event_client: EventBusClient) -> None:
        """ Force a default event client if the caller prefers to create their own instead of using the
        get_default_event_client() method. It is recommended that the caller not use this method unless necessary.

        :param event_client: The event client to use as the default.
        """
        cls._default_event_client = event_client


def put_datahex_event(detail_type: str, detail: dict, event_bus_client: EventBusClient = None) -> None:
    """ Put a DataHex event onto the default DataHex event bus.

    :param detail_type: The type of event to put.
    :param detail: The detail payload of the event.
    :param event_bus_client: Optional event client to use when putting an event (use default one if not specified).
    """
    if not event_bus_client:
        event_bus_client = DataHexEventBusClient.get_default_event_client()

    event_bus_client.put_event(detail_type, detail)


def send_event_to_bus(bus_name: str, source: str, detail_type: str, detail: Dict) -> None:
    """ Send an event to an EventBridge bus.

    :param bus_name: Name of the event bus (needs to be the actual event bus name).
    :param source: Source of the event.
    :param detail_type: Detail type of the event.
    :param detail: The content of the detail to send.
    :return: None
    """
    EventBusClient(bus_name, source).put_event(detail_type, detail)
