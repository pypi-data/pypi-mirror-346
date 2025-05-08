from typing import List, Dict, Any

from fastapi import HTTPException

from redis_tools.schema import RedisKeyInfo


class RedisConnection:
    def __init__(self):
        # Get settings from config
        from .config import RedisToolsSettings
        settings = RedisToolsSettings()

        # Create Redis client with settings
        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password,
            decode_responses=settings.redis_decode_responses
        )

    def test_connection(self) -> bool:
        try:
            return self.client.ping()
        except redis.exceptions.ConnectionError:
            return False

    def get_key_info(self, key: str) -> RedisKeyInfo:
        key_type = self.client.type(key)
        ttl = self.client.ttl(key)

        preview = None
        size = None

        if key_type == "string":
            value = self.client.get(key)
            size = len(value) if value else 0
            preview = value[:100] if value else ""
        elif key_type == "list":
            size = self.client.llen(key)
            preview = str(self.client.lrange(key, 0, 5))
        elif key_type == "hash":
            size = self.client.hlen(key)
            preview = str(dict(list(self.client.hgetall(key).items())[:5]))
        elif key_type == "set":
            size = self.client.scard(key)
            preview = str(self.client.smembers(key)[:5] if size <= 5 else list(self.client.smembers(key))[:5])
        elif key_type == "zset":
            size = self.client.zcard(key)
            preview = str(self.client.zrange(key, 0, 5, withscores=True))

        return RedisKeyInfo(
            key=key,
            type=key_type,
            ttl=ttl,
            size=size,
            preview=preview
        )

    def get_keys(self, pattern: str = "*", limit: int = None) -> List[RedisKeyInfo]:
        from .config import RedisToolsSettings
        settings = RedisToolsSettings()

        # Use provided limit or default from settings
        if limit is None:
            limit = settings.keys_limit

        keys = self.client.keys(pattern)[:limit]
        return [self.get_key_info(key) for key in keys]

    def get_key_data(self, key: str) -> Dict[str, Any]:
        key_type = self.client.type(key)
        data = {
            "key": key,
            "type": key_type,
            "ttl": self.client.ttl(key),
        }

        if key_type == "string":
            data["value"] = self.client.get(key)
        elif key_type == "list":
            data["value"] = self.client.lrange(key, 0, -1)
        elif key_type == "hash":
            data["value"] = self.client.hgetall(key)
        elif key_type == "set":
            data["value"] = list(self.client.smembers(key))
        elif key_type == "zset":
            data["value"] = self.client.zrange(key, 0, -1, withscores=True)

        return data

    def delete_key(self, key: str) -> bool:
        return bool(self.client.delete(key))

    def flush_db(self) -> bool:
        self.client.flushdb()
        return True


def get_redis_connection():
    conn = RedisConnection()
    if not conn.test_connection():
        raise HTTPException(status_code=500, detail="Cannot connect to Redis server")
    return conn
