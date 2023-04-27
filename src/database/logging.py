import logging


from redis_log_handler import RedisKeyHandler

def setLogHandler():
    handler = RedisKeyHandler('api-logs', host="redis", port=6379, password=None)  # Default parameters for Redis connection are used

    logger = logging.getLogger()  # No name gives you the root logger
    logger.setLevel("DEBUG")
    logger.addHandler(handler)