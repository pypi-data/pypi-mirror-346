# corstream/ops/map.py

from typing import AsyncIterable, Callable, TypeVar, Union, Awaitable, cast
import asyncio

T = TypeVar("T")
U = TypeVar("U")

MapFunction = Callable[[T], Union[U, Awaitable[U]]]


def map_op(fn: MapFunction[T, U]) -> Callable[[AsyncIterable[T]], AsyncIterable[U]]:
    """
    Creates a mapping operator that applies a function to each item
    in the stream. Supports both sync and async functions.

    :param fn: A function (sync or async) to apply to each element.
    :return: A transformation function to apply to an AsyncIterable.
    """

    async def __inner(source: AsyncIterable[T]) -> AsyncIterable[U]:
        async for item in source:
            result = fn(item)
            if asyncio.iscoroutine(result):
                result = await result
            yield cast(U, result)

    return __inner
