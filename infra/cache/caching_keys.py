from typing import Optional

from fastapi_cache import FastAPICache
from starlette.requests import Request
from starlette.responses import Response


def function_kwargs_builder(*fields: str):
    """
    Provides an arbitrary number of keyword arguments to a cached function.
    """

    if fields is None:
        fields = ('',)

    def key_builder(
        func,
        namespace: Optional[str] = "",
        request: Request = None,
        response: Response = None,
        *args,
        **kwargs,
):
        prefix = FastAPICache.get_prefix()

        final_kwargs = [f'{field}:{kwargs['kwargs'][field]}' for field in fields if field in kwargs['kwargs']]
        final_kwargs = ','.join(final_kwargs)
        return f"{prefix}:{namespace}:{func.__module__}:{func.__name__}:{args}:{final_kwargs}:{request.query_params}:{request.headers['accept']}"

    return key_builder