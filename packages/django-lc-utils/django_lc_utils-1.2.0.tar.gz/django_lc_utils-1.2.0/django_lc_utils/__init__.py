import math
from functools import wraps
from random import randint


def round_up(n, decimals=2):
    multiplier = 10**decimals
    return math.floor(float(n) * multiplier + 0.5) / multiplier


def randN(N):
    min = pow(10, N - 1)
    max = pow(10, N) - 1
    return randint(min, max)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", None)
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def cached_attribute(func):
    cache_name = f"_{func.__name__}"

    @wraps(func)
    def inner(self, *args, **kwargs):
        if hasattr(self, cache_name):
            return getattr(self, cache_name)
        val = func(self, *args, **kwargs)
        setattr(self, cache_name, val)
        return val

    return inner
