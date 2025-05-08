# redis_browser.py

from pathlib import Path

import redis
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from fastpluggy.core.dependency import get_templates
from redis_tools.redis_connector import RedisConnection, get_redis_connection

# Create router
redis_router = APIRouter()


# Define routes
@redis_router.get("/browser", response_class=HTMLResponse)
async def redis_browser(request: Request, templates=Depends(get_templates)):
    return templates.TemplateResponse("redis_browser/browser.html.j2", {"request": request})

@redis_router.get("/keys")
async def get_keys(pattern: str = "*", redis_conn: RedisConnection = Depends(get_redis_connection)):
    return redis_conn.get_keys(pattern)

@redis_router.get("/keys/{key}")
async def get_key(key: str, redis_conn: RedisConnection = Depends(get_redis_connection)):
    return redis_conn.get_key_data(key)

@redis_router.delete("/keys/{key}")
async def delete_key(key: str, redis_conn: RedisConnection = Depends(get_redis_connection)):
    success = redis_conn.delete_key(key)
    return {"success": success}

@redis_router.post("/flush-db")
async def flush_db(redis_conn: RedisConnection = Depends(get_redis_connection)):
    success = redis_conn.flush_db()
    return {"success": success}
