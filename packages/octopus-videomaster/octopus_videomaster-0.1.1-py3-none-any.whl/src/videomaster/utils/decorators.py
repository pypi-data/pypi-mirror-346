"""装饰器模块"""

import time
import logging
from src.videomaster.utils.helpers import setup_logging


def runtime(func):
    """计算函数运行时间的装饰器"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"Function '{func.__name__}' took {duration:.4f} seconds to run.")
        return result

    return wrapper