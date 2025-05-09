"""
Copyright (c) 2019-2020 RoZetta Technology Pty Ltd. All rights reserved.
"""
import os
import uuid
import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

from .utils import get_logger
from .models import AWSEvent, AuditCommonFields, AuditException
from .component_service import get_source

logger = get_logger(__name__)

EVENT_VERSION = 'v1.0.0'  # event detail version number


# pylint: disable=too-few-public-methods
class AuditSession:

    def __init__(self, common_fields):
        self.common_fields = common_fields

    def _construct_audit_event(self, action, result, event_details):
        """
        Constructs AWSEvent object from passed-in information.

        :param action: String. The Action of the audit event.
        :param result: String. Result of the action.
        :param event_details: Dict. Other required details of the audit event.
        :return: returns AWSEvent object.
        """
        details = {}
        details['Time'] = datetime.utcnow().isoformat()
        details['Action'] = action
        details['Result'] = result
        details['EventVersion'] = EVENT_VERSION
        details['ExecutionID'] = self.common_fields.execution_id
        details['ParentExecutionID'] = self.common_fields.parent_execution_id
        details['Service'] = self.common_fields.service
        details['Component'] = self.common_fields.component
        details['Release'] = self.common_fields.release_version
        details = {**event_details, **details}
        detail = json.dumps(details)
        event = AWSEvent(source=self.common_fields.source, detail_type=action,
                         detail=detail, event_bus_name=self.common_fields.event_bus_name)
        return event

    def put_audit_event(self, action, result, event_details):
        """
        Push AWSEvent object into Event Bus.

        :param action: String. The Action of the audit event.
        :param result: String. Result of the action.
        :param event_details: Dict. Other required details of the audit event.
        :return: returns nothing.
        :raise: raises AuditException if fail to push the event.
        """
        eb = boto3.client('events')
        event = self._construct_audit_event(action, result, event_details)
        logger.info('sending audit event: %s', event.to_dict())
        try:
            r = eb.put_events(
                Entries=[event.to_dict()]
            )
            if r['FailedEntryCount'] != 0:
                raise AuditException('Failed to put audit event into EventBus')
        except ClientError as e:
            logger.error("Unexpected error: %s",  e)
            raise AuditException(
                'Failed to put audit event into EventBus') from e


# pylint: disable=too-few-public-methods
class AuditClient:

    def __init__(self, bus_name: str, event_bus_env_var_name: str, **kwargs):
        product = kwargs['product']
        environment = kwargs['environment']
        service = kwargs['service']
        component = kwargs['component']
        release_version = kwargs['release_version']
        parent_execution_id = kwargs.get('parent_execution_id')
        event_bus_full_name = kwargs.get('event_bus_name') or os.getenv(event_bus_env_var_name)
        if not event_bus_full_name:
            # An explicit event bus name was not specified so lets attempt to evaluate using the 'product' and 'env'.
            prod = product or os.getenv("PRODUCT")
            env = environment or os.getenv("ENV")
            if prod and env and bus_name:
                event_bus_full_name = f"{prod}-{env}-{bus_name}"
            else:
                logger.error("Event bus '%s' is not correctly setup", bus_name)
        source = get_source(component)
        self.common_fields = AuditCommonFields(event_bus_name=event_bus_full_name, source=source, service=service,
                                               component=component, release_version=release_version,
                                               parent_execution_id=parent_execution_id)

    def start_audit(self):
        """"
        Starts with a new audit session with new unique execution ID.

        :return: returns AuditSession instance.
        """
        # generate
        execution_id = str(uuid.uuid4())
        logger.info('Generated execution ID: %s', execution_id)
        self.common_fields.execution_id = execution_id
        return AuditSession(self.common_fields)


AUDIT_EVENT_BUS_NAME = "AuditEventBus"


def audit_event_client(**kwargs):
    """ Prepare an EventClient object that can be used by DataHex components to publish a `Audit Event`
    onto the `AuditEventBus`.

    :param kwargs: contains the common fields as per `AuditCommonFields` data class.
    :type kwargs: keyword args
    :return: An event client that can be used to publish "audit events".
    :rtype: AuditClient
    """
    return AuditClient(AUDIT_EVENT_BUS_NAME, "AUDIT_EVENT_BUS_NAME", **kwargs)
