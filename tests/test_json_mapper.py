import os
import unittest
from dataclasses import dataclass

from config_dataclass_mapper.json_mapper import JsonFileMapper
from config_dataclass_mapper.serializable import Serializable


@JsonFileMapper(json_file_path='./conf_files/db.json')
@dataclass
class PostgresDBConf(Serializable):
    host: str
    port: int


class TestJsonMapper(unittest.TestCase):
    def test_basic_mapper(self):
        db_conf = PostgresDBConf()
        self.assertEqual(db_conf.host, 'localhost')


if __name__ == '__main__':
    unittest.main()
