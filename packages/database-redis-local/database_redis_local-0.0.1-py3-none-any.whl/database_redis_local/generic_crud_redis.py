import redis
# import json
# import uuid
from typing import Optional

from python_sdk_remote.utilities import our_get_env


class GenericCrudRedis:
    """A Redis version of GenericCRUD using Redis hashes for storage."""

    def __init__(self, default_schema_name: str, default_table_name: Optional[str] = None,
                 default_column_name: str = "id", is_test_data: bool = False):
        self.default_schema_name = default_schema_name
        self.default_table_name = default_table_name or "default_table"
        self.default_column_name = default_column_name
        self.is_test_data = is_test_data
        self.hostname = our_get_env("REDIS_HOSTNAME")
        self.port = our_get_env("REDIS_PORT")
        self.password = our_get_env("REDIS_PASSWORD")
        self.redis = redis.Redis(host=self.hostname, port=self.port,
                                 password=self.password, db=0,
                                 decode_responses=True)
        self.id_key = f"{self.default_schema_name}:{self.default_table_name}:id"  # For ID increment

    def _make_key(self, id_value: str) -> str:
        return f"{self.default_schema_name}:{self.default_table_name}:{id_value}"

    def _generate_id(self) -> int:
        return self.redis.incr(self.id_key)

    def insert(self, data_dict: dict, ignore_duplicate: bool = False) -> int:
        # Attempt to find an exact match if ignore_duplicate is set
        if ignore_duplicate:
            existing_id = self._find_duplicate(data_dict)
            if existing_id is not None:
                return existing_id

        new_id = self._generate_id()
        data_dict[self.default_column_name] = new_id
        key = self._make_key(new_id)

        self.redis.hset(key, mapping=data_dict)
        return new_id

    def read(self, id_value: int) -> dict:
        key = self._make_key(id_value)
        return self.redis.hgetall(key)

    def update(self, id_value: int, update_dict: dict) -> bool:
        key = self._make_key(id_value)
        if not self.redis.exists(key):
            return False
        self.redis.hset(key, mapping=update_dict)
        return True

    def delete(self, id_value: int) -> bool:
        key = self._make_key(id_value)
        return self.redis.delete(key) == 1

    def _find_duplicate(self, data_dict: dict) -> Optional[int]:
        # Inefficient, just for demonstration: scan all keys in this schema/table
        pattern = f"{self.default_schema_name}:{self.default_table_name}:*"
        for key in self.redis.scan_iter(pattern):
            existing_data = self.redis.hgetall(key)
            if all(str(existing_data.get(k)) == str(v) for k, v in data_dict.items()):
                return int(existing_data[self.default_column_name])
        return None
