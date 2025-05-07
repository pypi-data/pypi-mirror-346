# corstream/ops/filter.py

from typing import AsyncIterable, AsyncIterator, Callable, TypeVar, Union, Awaitable
import asyncio

T = TypeVar("T")
Predicate = Callable[[T], Union[bool, Awaitable[bool]]]


def filter_op(
    predicate: Predicate[T],
) -> Callable[[AsyncIterable[T]], AsyncIterable[T]]:
    """
    Creates a filter operator that passes through only items
    for which the predicate returns True.

    :param predicate: A boolean function (sync or async).
    :return: A transformation function to apply to an AsyncIterable.
    """

    async def _inner(source: AsyncIterable[T]) -> AsyncIterator[T]:
        async for item in source:
            result = predicate(item)
            if asyncio.iscoroutine(result):
                result = await result
            if result:
                yield item

    return _inner
