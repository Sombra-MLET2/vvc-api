from aiocache import cached


def __cache_key():
    """
    Provides an arbitrary number of keyword arguments to a cached function.
    """

    def key_builder(
        func,
        *args,
        **kwargs,
):
        cache_args = ';'.join([str(arg) for arg in args if isinstance(arg, (str, int, float))])

        return f"{func.__name__}:{cache_args}"

    return key_builder

def vvc_cache(ttl=600):
    def decorator(func):
        @cached(ttl=ttl, key_builder=__cache_key())
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        return wrapper

    return decorator