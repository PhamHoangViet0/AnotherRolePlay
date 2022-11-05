from functools import wraps
from . import ajax


def have_ajax(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        if args[0].headers.get('x-requested-with') == 'XMLHttpRequest':
            return getattr(ajax, function.__name__)(*args, **kwargs)
        else:
            return function(*args, **kwargs)
    return decorator