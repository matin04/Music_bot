from utils.redis_client import redis_client


def cache_song(
    query: str,
    path: str
):

    redis_client.set(
        query,
        path,
        ex=60 * 60 * 24
    )


def get_cached_song(
    query: str
):

    return redis_client.get(query)