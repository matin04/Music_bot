import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, cooldown_seconds: int = 5):
        self.cooldown = cooldown_seconds
        self.users = defaultdict(float)

    def is_allowed(self, user_id: int) -> bool:
        now = time.time()
        last_time = self.users[user_id]

        if now - last_time < self.cooldown:
            return False

        self.users[user_id] = now
        return True