import logging
import os
import sys
from datetime import datetime
from functools import wraps

LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.DEBUG)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))
logger.setLevel(LOG_LEVEL)


def log(sep='\t', level=logging.INFO, log_args=True, log_return=True):
    def _log(func: callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_timestamp = datetime.now().timestamp() * 1000
            start = f'Start{sep}{func.__module__}.{func.__qualname__}'
            if log_args:
                start += f'{sep}args={args}{sep}kwargs={kwargs}'
            logger.log(level, start)

            result = func(*args, **kwargs)

            end_timestamp = datetime.now().timestamp() * 1000
            duration = int(end_timestamp - start_timestamp)
            end = f'End{sep}{func.__module__}.{func.__qualname__}{sep}{duration} ms'
            if log_return:
                end += f'{sep}result={result}'
            logger.log(level, end)

            return result
        return wrapper
    return _log
