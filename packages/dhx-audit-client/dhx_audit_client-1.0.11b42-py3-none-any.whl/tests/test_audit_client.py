"""
 Copyright (c) 2019 - 2020 Rozetta Technology Pty Ltd. All rights reserved.
"""
import pytest
from botocore.exceptions import ClientError

from audit_client.component_service import get_source
from audit_client.audit_client import audit_event_client
from audit_client.models import AuditException


@pytest.fixture()
def mock_boto3(mocker, monkeypatch):
    mock = mocker.Mock()
    mock.client = mocker.patch("boto3.client")
    return mock


def test_component_service():
    assert get_source('ftp_downloader') is not None
    assert get_source('') == 'undefined_source'


def test_audit_client(mocker, mock_boto3):
    mock_eb = mocker.Mock()
    mock_boto3.client.side_effect = [mock_eb]
    mock_eb.put_events.return_value = {'FailedEntryCount': 0,
                                       'Entries': [{'EventId': 'event-id-1234'}]}
    product = 'dhx'
    environment = 'dev'
    service = 'datahex_downloader'
    component = 'ftp_downloader'
    release_version = 'v0.0.1'
    audit_client = audit_event_client(product=product, environment=environment, service=service,
                               component=component, release_version=release_version)
    session = audit_client.start_audit()
    action = 'SourceConnectionStartDetail'
    result = 'CONNECTION_REFUSED'
    event_details = {'Host': 'ftp://ftp.morningstar.com/'}

    session.put_audit_event(action, result, event_details)
