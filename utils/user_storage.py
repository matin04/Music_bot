from utils.redis_client import redis_client


def save_user_link(
    user_id: int,
    link: str
):

    redis_client.set(
        f"user:{user_id}",
        link,
        ex=3600
    )


def get_user_link(
    user_id: int
):

    return redis_client.get(
        f"user:{user_id}"
    )


def delete_user_link(
    user_id: int
):

    redis_client.delete(
        f"user:{user_id}"
    )