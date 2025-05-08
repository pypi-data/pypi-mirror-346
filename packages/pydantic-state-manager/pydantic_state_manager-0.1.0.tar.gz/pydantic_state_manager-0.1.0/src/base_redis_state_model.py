from pydantic import BaseModel, TypeAdapter, ValidationError
import uuid

from redis_client import redis_client


class BaseRedisStateModel(BaseModel, arbitrary_types_allowed=True):
    id_: str = str(uuid.uuid4())

    def __init__(self, **data):
        super().__init__(**data)
        # if id is not provided, generate a new one
        self._redis_key = f"{self.__class__.__name__}:{self.id_}"
        # check if the key exists in Redis
        if not redis_client.exists(self._redis_key):
            redis_client.hset(self._redis_key, mapping=self.model_dump())

    def __setattr__(self, key, value):
        if key in self.model_fields:
            redis_client.hset(self._redis_key, mapping={key: value})
        super().__setattr__(key, value)

    def __getattribute__(self, key):
        val = super().__getattribute__(key)
        if key not in {"model_fields", "id_"} and key in self.model_fields:
            redis_val = self.__get_current_attribute_value(key)
            if isinstance(redis_val, (bytes, bytearray)):
                redis_val = redis_val.decode("utf-8")
            type_adapter = self.__get_type_adapter(key)
            redis_val = self.__validate_value(type_adapter, redis_val)
            if redis_val != val:
                setattr(self, key, redis_val)
            return redis_val
        return val

    def __get_current_attribute_value(self, key_name: str):
        return redis_client.hget(self._redis_key, key_name)

    def __get_type_adapter(self, key_name: str):
        val_type = self.model_fields[key_name].annotation
        val_type = TypeAdapter(val_type)
        return val_type

    def __validate_value(self, type_adapter: TypeAdapter, row_value):
        try:
            return type_adapter.validate_python(row_value)
        except ValidationError:
            return type_adapter.validate_json(row_value)
