import logging
import time
from collections import deque

logger = logging.getLogger(__name__)


class RateLimiter:
    def __init__(self, tokens_per_second=0.25, max_tokens=1.0, hourly_limit=24):
        self.tokens_per_second = tokens_per_second
        self.max_tokens = max_tokens
        self.tokens = 1.0
        self.last_update = time.time()
        # Track hourly requests
        self.hourly_limit = hourly_limit
        self.request_times = deque()  # Store timestamps of requests

    def _add_new_tokens(self):
        now = time.time()
        time_passed = now - self.last_update
        new_tokens = time_passed * self.tokens_per_second
        self.tokens = min(self.max_tokens, self.tokens + new_tokens)
        self.last_update = now

    def _sleep_if_needed(self):
        if self.tokens < 1.0:
            sleep_time = (1.0 - self.tokens) / self.tokens_per_second
            logger.debug(f"Rate limit reached, sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)

    def _check_hourly_limit(self):
        now = time.time()
        if len(self.request_times) >= self.hourly_limit:
            # Calculate time to wait until oldest request expires
            wait_time = 3600 - (now - self.request_times[0])
            logger.debug(f"Hourly limit reached, waiting {wait_time:.2f} seconds")
            time.sleep(wait_time)
            # Remove expired requests
            while self.request_times and now - self.request_times[0] > 3600:
                self.request_times.popleft()

    def acquire(self):
        """Acquire a token, wait if necessary"""
        self._add_new_tokens()
        self._sleep_if_needed()
        self._check_hourly_limit()

        self.tokens -= 1.0
        self.request_times.append(time.time())
        return True
