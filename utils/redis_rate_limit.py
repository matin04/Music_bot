from utils.redis_client import redis_client


class RedisRateLimiter:

    def is_allowed(
        self,
        user_id: int,
        limit=5
    ):

        key = f"rate:{user_id}"

        current = redis_client.get(key)

        if current:

            return False

        redis_client.set(
            key,
            1,
            ex=limit
        )

        return True