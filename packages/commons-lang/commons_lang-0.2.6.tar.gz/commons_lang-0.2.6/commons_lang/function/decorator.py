import time as t

from loguru import logger


def time(func):
    def wrapper(*args, **kwargs):
        start_time = t.time()
        result = func(*args, **kwargs)
        end_time = t.time()
        logger.deb(f"{func.__name__} elapsed time: {end_time - start_time:.4f} s")
        return result

    return wrapper
