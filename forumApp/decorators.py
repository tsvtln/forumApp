import time
from functools import wraps


def measure_execution_time(view_function):
    @wraps(view_function)
    def _wrapper(request, *args, **kwargs):
        start_time = time.time()
        result = view_function(request, *args, **kwargs)
        end_time = time.time()
        print(f"The time it took for {view_function.__name__}: ", end_time - start_time, "seconds")

        return result
    return _wrapper
