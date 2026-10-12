import json

from langchain_classic.utilities import redis


async def get_user_info(user_id: int):
    cache_key = f"user:{user_id}"

    # 1. 拿数据：先去 Redis 查
    data = await redis.get(cache_key)

    # 2. 如果拿到了，直接返回
    if data:
        return json.loads(data)

    # 3. 没拿到，去数据库查
    data = await db.query("SELECT * FROM users WHERE id = %s", user_id)

    # 4. 存内存：顺手备份到 Redis（设置 60 秒后自动过期）
    await redis.set(cache_key, json.dumps(data), ex=60)

    # 5. 返回结果
    return data