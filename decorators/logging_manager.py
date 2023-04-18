# import functools
import logging
from logging.handlers import TimedRotatingFileHandler

from datetime import datetime
import time
import os
import sys

import inspect


def now(): return datetime.now().strftime('%F %X')


logDir = 'logs'

# normal/TimedRotating Choose logging Handler between straight Handler and TimedRotatingHandler
logging_type = 'normal'

frame = inspect.stack()[-1]
caller_filename = frame[0].f_code.co_filename
log_basename = os.path.splitext(os.path.basename(caller_filename))[0]

try:
    os.mkdir(logDir)
except Exception as e:
    pass


scriptName = os.path.basename(sys.argv[0].replace('.py', ''))
LOG_FORMAT = '[%(asctime)s] %(levelname)8s - %(name)s - %(message)s'
# LOG_FORMAT = logging.Formatter(LOG_FORMAT, '%Y-%m-%d %H:%M:%S')

if logging_type == 'TimedRotating':
    logFileName = logDir + os.sep + \
        '{}.log'.format(log_basename)
    Handler = TimedRotatingFileHandler(logFileName, when="midnight", interval=1, encoding='utf-8', backupCount=30)
else:
    logFileName = logDir + os.sep + \
        '{}_{}.log'.format(log_basename, datetime.now().strftime('%F'))
    Handler = logging.FileHandler(logFileName, 'a', 'utf-8')


logging.basicConfig(handlers=[Handler],
                    level=logging.INFO,
                    format=LOG_FORMAT,
                    datefmt='%F %X',
                    )
logger = logging.getLogger(scriptName)


def log_msg(msg='', logLevel='INFO', print_flg=True):
    ''' 
    Log custom msg

    Use "from logging_manager import log_msg as print" to replace print function in old scripts
    '''
    logLevelList = ['debug', 'info', 'warning', 'error', 'critical', ]
    if logLevel.lower() in logLevelList:
        eval('logging.{}({!r})'.format(logLevel.lower(), msg))
        if print_flg:
            print(msg)


def logging_to_file(func):
    """
    A decorator that wraps the passed in func and logs 
    exceptions should one occur

    @logging_manager.logging_to_file
    """
    # @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # logger = create_logger()
        try:
            t1 = time.time()
            logger.info('{} starts on {}'.format(func.__name__, now()))

            func_args = inspect.signature(func).bind(*args, **kwargs).arguments
            func_args_str = ', '.join('{} = {!r}'.format(*item)
                                      for item in func_args.items())
            logger.debug('{}.{} ({})'.format(
                func.__module__, func.__qualname__, func_args_str))

            x = func(*args, **kwargs)
        except:
            # log the exception
            err = "There was an exception in {}".format(func.__name__)
            logger.exception(err)

            # re-raise the exception
            raise
        else:
            return x
        finally:
            t2 = time.time()
            logger.info('{} ends on {}, duration: {}s\n'.format(
                func.__name__, now(), round(t2 - t1, 3)))
    return wrapper


if __name__ == '__main__':
    for x in range(100):
        log_msg('new is {}'.format(now()))
        time.sleep(5)
    # print(dir(logging))
    # print(logging.getLevelName('d'))
