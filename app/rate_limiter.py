import logging
import time

logger = logging.getLogger(__name__)


class RateLimiter:
    def __init__(self, tokens_per_second=0.25, max_tokens=1.0):
        self.tokens_per_second = tokens_per_second
        self.max_tokens = max_tokens
        self.tokens = 1.0
        self.last_update = time.time()

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

    def acquire(self):
        """Acquire a token, wait if necessary"""
        self._add_new_tokens()
        self._sleep_if_needed()
        self.tokens -= 1.0
        return True
