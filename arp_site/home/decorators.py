from functools import wraps


def logged(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        print("%s.%s called" % (function.__module__, function.__name__))
        return function(*args, **kwargs)
    return decorator
