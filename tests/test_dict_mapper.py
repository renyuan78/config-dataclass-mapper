import unittest
from dataclasses import dataclass

from config_dataclass_mapper.dict_mapper import DictMapper
from config_dataclass_mapper.serializable import Serializable

dict_config_data = {
    'host': 'localhost',
    'port': 5432
}


@DictMapper(conf_dict=dict_config_data)
@dataclass
class PostgresDB(Serializable):
    host: str
    port: int


class TestDictMapper(unittest.TestCase):
    def test_basic_mapper(self):
        pg = PostgresDB()
        self.assertEqual(pg.port, 5432)

    def test_to_json(self):
        pg = PostgresDB()
        dump = pg.to_json()
        self.assertTrue(dump.__class__.__name__ == 'str')


if __name__ == '__main__':
    unittest.main()
