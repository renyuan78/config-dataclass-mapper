import json

from config_dataclass_mapper.dict_mapper import DictMapper


class JsonFileMapper(DictMapper):
    def __init__(self, json_file_path: str):
        with open(json_file_path) as f:
            dt = json.loads(f.read())
            super().__init__(conf_dict=dt)
