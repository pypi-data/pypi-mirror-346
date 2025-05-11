import unittest
from dataclasses import dataclass

from src.alt_utils import NestedDeserializableDataclass


@dataclass
class DatabaseConfig:
    db: str
    user: str
    password: str
    host: str
    port: int = 5432


@dataclass
class AuthConfig:
    user: str
    password: str


@dataclass
class SomeVal:
    val: str


@dataclass
class Config(NestedDeserializableDataclass):
    database: DatabaseConfig
    valid_auths: list[AuthConfig]
    some_other_vals: dict[str, SomeVal]
    misc: str


class TestDataStructures(unittest.TestCase):
    def test_nested_serializable_dataclass(self):
        config_dict = {
            "database": {"db": "dbname", "user": "username", "host": "hostname", "password": "rosebud"},
            "valid_auths": [
                {"user": "user1", "password": "pwhash1"},
                {"user": "user2", "password": "pwhash2"},
            ],
            "some_other_vals": {
                "val1": {"val": "val1"},
            },
            "misc": "something",
        }
        config_gen = Config.from_dict(config_dict)
        config_manual = Config(
            database=DatabaseConfig(db="dbname", user="username", host="hostname", password="rosebud", port=5432),
            valid_auths=[
                AuthConfig(user="user1", password="pwhash1"),
                AuthConfig(user="user2", password="pwhash2"),
            ],
            some_other_vals={"val1": SomeVal(val="val1")},
            misc="something",
        )
        self.assertEqual(config_gen, config_manual)
