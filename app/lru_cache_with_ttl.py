from collections import OrderedDict
import time
import logging

logger = logging.getLogger(__name__)


class LRUCacheWithExpiration(OrderedDict):
    """LRU Cache with size limit and expiration"""

    def __init__(self, maxsize=100, ttl=12 * 3600):
        super().__init__()
        self.maxsize = maxsize
        self.ttl = ttl

    def __getitem__(self, key):
        """Get item and check expiration

        Note: dont call this directly, use get method instead...
        cache[key] = value is not recommended, can raise Error if expired or not found
        """
        value, timestamp = super().__getitem__(key)
        if time.time() - timestamp > self.ttl:
            del self[key]
            raise KeyError(f"Cache entry expired for {key}")
        self.move_to_end(key)  # Move to end (most recently used)
        return value, timestamp

    def __setitem__(self, key, value):
        """Set item with timestamp and enforce size limit"""
        if key in self:
            self.move_to_end(key)
        super().__setitem__(key, value)
        if len(self) > self.maxsize:
            oldest = next(iter(self))  # Get first item (least recently used)
            del self[oldest]

    def get(self, key, default=None):
        """Get item with expiration check"""
        try:
            return self[key]
        except KeyError:
            return default
