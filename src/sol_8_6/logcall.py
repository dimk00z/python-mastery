from functools import wraps

from src.sol_7_2.validate import Integer, enforce


def logformat(fmt):
    def logged(func):
        print("Adding logging to", func.__name__)

        @wraps(func)
        def wrapper(*args, **kwargs):
            print(fmt.format(func=func))
            return func(*args, **kwargs)

        return wrapper

    return logged


logged = logformat("Calling {func.__name__}")


@logged
@enforce(x=Integer, y=Integer, return_=Integer)
def add(x, y):
    "Adds two things"
    return x + y
