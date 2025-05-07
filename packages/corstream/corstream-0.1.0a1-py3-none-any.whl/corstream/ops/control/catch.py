# corstream/ops/control/catch.py

from typing import AsyncIterable, AsyncIterator, Callable, TypeVar, Optional

T = TypeVar("T")


def catch_op(
    handler: Callable[[Exception], Optional[T]]
) -> Callable[[AsyncIterable[T]], AsyncIterable[T]]:
    """
    Catches exceptions during iteration and applies a handler function.
    The handler can return a replacement value or None to skip the item.

    :param handler: A function that receives the exception and optionally returns a fallback value.
    :return: A new async iterable with error handling applied.
    """

    async def _inner(source: AsyncIterable[T]) -> AsyncIterator[T]:
        async for item in source:
            try:
                yield item
            except Exception as e:
                fallback = handler(e)
                if fallback is not None:
                    yield fallback
                # else: item is skipped silently

    return _inner
