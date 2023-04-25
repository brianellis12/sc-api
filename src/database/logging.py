from redis import Redis
import logging
import sys

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

# Add a StreamHandler to log messages to the console
console_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(console_handler)

# Replace the URL with the one provided in the docker-compose file
redis_url = "redis://eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81@redis:6379"
redis_client = Redis.from_url(redis_url)

class RedisLoggingHandler(logging.Handler):
    def __init__(self, redis_client):
        super().__init__()
        self.redis_client = redis_client

    def emit(self, record):
        log_entry = self.format(record)
        self.redis_client.rpush("logs", log_entry)

# Add the RedisLoggingHandler to the logger
redis_handler = RedisLoggingHandler(redis_client)

logger.addHandler(redis_handler)
