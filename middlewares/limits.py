from collections import defaultdict
from datetime import datetime

downloads = defaultdict(list)

FREE_LIMIT = 5


def can_download(user_id):

    now = datetime.now()

    today = now.date()

    downloads[user_id] = [
        d for d in downloads[user_id]
        if d.date() == today
    ]

    return len(downloads[user_id]) < FREE_LIMIT


def add_download(user_id):

    downloads[user_id].append(
        datetime.now()
    )