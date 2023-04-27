import time


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter_ns()
        result = func(*args, **kwargs)
        stop_time = time.perf_counter_ns() - start_time
        return (result, stop_time)
    return wrapper
