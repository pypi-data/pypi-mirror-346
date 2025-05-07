# corstream/sinks/for_each.py

from typing import AsyncIterable, Callable, Awaitable, TypeVar, Union
import asyncio

T = TypeVar("T")
Consumer = Callable[[T], Union[None, Awaitable[None]]]


async def for_each_sink(source: AsyncIterable[T], fn: Consumer[T]) -> None:
    """
    Terminal sink that consumes each item in the stream and applies
    a side-effect function (sync or async).

    :param source: The async iterable to consume.
    :param fn: The function to apply to each item (may be async).
    """
    async for item in source:
        result = fn(item)
        if asyncio.iscoroutine(result):
            await result
