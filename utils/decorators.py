import datetime
from functools import wraps


def execution_time(func):
    @wraps(func)
    def timer(*args, **kwargs):
        time = datetime.datetime.now()
        func(*args, **kwargs)
        print('Execution time: {time}'.format(time=datetime.datetime.now()-time))
        return func
    return timer
