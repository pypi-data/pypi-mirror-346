"""
Copyright (c) 2019-2020 RoZetta Technology Pty Ltd. All rights reserved.
"""
import pprint
from datetime import datetime
from dataclasses import dataclass, fields, field
from typing import List


class AuditException(Exception):
    pass


@dataclass
class AWSEvent:

    _field_mappings = {
        'event_bus_name': 'EventBusName',
        'detail': 'Detail',
        'source': 'Source',
        'detail_type': 'DetailType',
        'resource': 'Resources',
        'time': 'Time'
    }

    event_bus_name: str
    detail: str
    source: str
    detail_type: str
    resource: List[str] = field(default_factory=list)
    time: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self):
        result = {}
        for attr_val in fields(self):
            attr = attr_val.name
            value = getattr(self, attr)
            mapped_field = self._field_mappings[attr]
            if isinstance(value, list):
                result[mapped_field] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            else:
                result[mapped_field] = value
        return result

    def to_str(self):
        return pprint.pformat(self.to_dict())


@dataclass
class AuditCommonFields:
    event_bus_name: str
    source: str
    service: str
    component: str
    release_version: str
    execution_id: str = ''
    parent_execution_id: str = ''
