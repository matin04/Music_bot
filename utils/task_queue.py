import asyncio
from collections import deque

class TaskQueue:
    def __init__(self):
        self.queue = deque()
        self.processing = False

    def add_task(self, coro):
        self.queue.append(coro)

    async def worker(self):
        while True:
            if self.queue:
                task = self.queue.popleft()
                try:
                    await task
                except Exception as e:
                    print(f"Queue error: {e}")
            else:
                await asyncio.sleep(0.5)