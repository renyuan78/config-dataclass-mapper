import unittest
from dataclasses import dataclass

from config_dataclass_mapper.dict_mapper import DictMapper
from config_dataclass_mapper.serializable import Serializable

db_config = {
    'host': 'localhost',
    'port': 5432
}


@DictMapper(conf_dict=db_config)
@dataclass
class PostgresDBConf(Serializable):
    host: str
    port: int


app_config = {
    'db_user_name': 'user',
    'db_password': "password",
    'db_name': 'app_db_name'
}


@DictMapper(conf_dict=app_config)
@dataclass
class AppConf(Serializable):
    db_user_name: str
    db_password: str
    db_name: str
    db: PostgresDBConf = PostgresDBConf()


class TestDictMapper(unittest.TestCase):
    def test_basic_mapper(self):
        pg = PostgresDBConf()
        self.assertEqual(pg.port, 5432)

    def test_to_json(self):
        pg = PostgresDBConf()
        dump = pg.to_json()
        self.assertTrue(dump.__class__.__name__ == 'str')

    def test_aggregate(self):
        app_conf = AppConf()
        self.assertEqual(app_conf.db_name, 'app_db_name')
        self.assertEqual(app_conf.db.port, 5432)


if __name__ == '__main__':
    unittest.main()
