import dataclasses
from datetime import datetime


class DictMapper(object):
    support_python_types: list = ['NoneType', 'str', 'int', 'float', 'list',
                                  'dict', 'tuple', 'bool', 'date', 'time', 'datetime']

    def __init__(self, conf_dict: dict, item_path: str = None, item_path_sep: str = '/'):
        self.item_conf = conf_dict

        if item_path is not None:
            items = item_path.lstrip(item_path_sep).rstrip(item_path_sep).split(item_path_sep)
            for item in items:
                self.item_conf = self.item_conf[item]

    def __call__(self, cls):
        missing_attr = DictMapper.__get_missing_attr_names(cls)

        # Set all missing attrs to None
        missing_attr_values = len(missing_attr) * [None]

        def wrapped_cls(*args, **kwargs):
            obj = cls(*missing_attr_values, *args, **kwargs)

            class_variables = [attr for attr in missing_attr if
                               not callable(getattr(obj, attr)) and
                               not attr.startswith("__") and
                               getattr(obj, attr).__class__.__name__ in DictMapper.support_python_types]

            for cv in class_variables:
                setattr(obj,
                        cv,
                        DictMapper.__get_item_value(obj, cv, self.item_conf[cv]) if cv in self.item_conf else None)

            return obj
        return wrapped_cls

    @staticmethod
    def __get_missing_attr_names(cls) -> list:
        fields = cls.__dict__['__dataclass_fields__']
        missing_attr_names = list(
            map(
                lambda x: fields[x].name,
                filter(
                    lambda x: type(fields[x].default) == dataclasses._MISSING_TYPE,
                    fields)
            ))

        return missing_attr_names

    @staticmethod
    def __get_item_value(obj, obj_attr_name, json_attr_value):
        attr_type = getattr(obj, obj_attr_name).__class__.__name__
        if attr_type == 'date':
            return DictMapper.__str_to_date(json_attr_value)
        elif attr_type == 'time':
            return DictMapper.__str_to_time(json_attr_value)
        elif attr_type == 'datetime':
            return DictMapper.__str_to_datetime(json_attr_value)
        else:
            return json_attr_value

    @staticmethod
    def __str_to_time(s):
        return datetime.strptime(s, '%H:%M:%S.%f').time()

    @staticmethod
    def __str_to_date(s):
        return datetime.strptime(s, '%Y-%m-%d').date()

    @staticmethod
    def __str_to_datetime(s):
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%f')
