# config-dataclass-mapper
Map configuration files(JSON, YAML, etc.) to Python data classes

## Map Python Dict to Data class
```
db_config = {
    'host': 'localhost',
    'port': 5432
}

@DictMapper(conf_dict=db_config)
@dataclass
class PostgresDBConf(Serializable):
    host: str
    port: int
```

## Map Json file to Data class
Make sure field names in data class should be as same as field names in JSON file
```
@DictMapper(json_file_path='your_json_file_path')
@dataclass
class PostgresDBConf(Serializable):
    host: str
    port: int
```

## Map a field in a JSON file to Data class
```
@DictMapper(json_file_path='your_json_file_path', item_path='/root/a/b', item_path_sep='/')
@dataclass
class PostgresDBConf(Serializable):
    host: str
    port: int
```

## Aggregate existing data classes
```
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
```

## Use default values in data class to ignore values in config
```
db_config = {
    'host': 'localhost',
    'port': 5432
}

@DictMapper(conf_dict=db_config)
@dataclass
class PostgresDBConf(Serializable):
    host: str = '10.10.0.1'
    port: int
```
In this case, the value of config `db_config.host` will be ignored
