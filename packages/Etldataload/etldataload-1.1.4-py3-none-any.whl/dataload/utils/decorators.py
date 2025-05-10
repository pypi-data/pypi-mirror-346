import functools
import time
import dataload.utils.logger as log

def timer(func):
    """print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer

def logger(func):
    """print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_logger(*args, **kwargs):
        (log
         .Logger()
         .debug('processing start....')
         )
        value = func(*args, **kwargs)
        (log
         .Logger()
         .debug('processing finish....')
         )
        return value
    return wrapper_logger

def slow_down(func):
    """print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_slow_down(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)
    return wrapper_slow_down

