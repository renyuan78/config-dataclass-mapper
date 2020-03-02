import json
from datetime import date, time, datetime


class Serializable:
    def to_json(self, indent: int = 4, sort_keys: bool = True):
        return json.dumps(self, default=Serializable.serialize, indent=indent, sort_keys=sort_keys)

    @staticmethod
    def serialize(obj):
        if isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, time):
            return obj.isoformat()
        elif isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return obj.__dict__
