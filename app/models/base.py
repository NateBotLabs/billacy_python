from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.inspection import inspect
from datetime import datetime
from enum import Enum
import json


class Base(DeclarativeBase):
    def to_dict(self):
        data = {}
        mapper = inspect(self.__class__)

        # Serialize columns
        for column in mapper.columns:
            key = column.key
            value = getattr(self, key)

            if isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, Enum):
                data[key] = value.value
            else:
                data[key] = value

        # Serialize relationships
        for rel in mapper.relationships:
            rel_value = getattr(self, rel.key)

            if rel_value is None:
                data[rel.key] = None

            elif rel.uselist:  # list of related models
                data[rel.key] = [
                    item.to_dict() if hasattr(item, "to_dict") else item
                    for item in rel_value
                ]

            else:  # single related model
                if hasattr(rel_value, "to_dict"):
                    data[rel.key] = rel_value.to_dict()
                else:
                    data[rel.key] = rel_value

        return data

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(), indent=2, **kwargs)
    pass
