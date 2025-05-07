# corstream/ops/diagnostic/log.py

from typing import AsyncIterable, AsyncIterator, TypeVar, Optional, Callable

T = TypeVar("T")


def log_op(
    label: Optional[str] = None,
) -> Callable[[AsyncIterable[T]], AsyncIterable[T]]:
    """
    Logs each item in the stream with an optional label, for debugging purposes.

    :param label: A string prefix to include in log output.
    :return: A passthrough async iterable that logs items.
    """

    async def _inner(source: AsyncIterable[T]) -> AsyncIterator[T]:
        async for item in source:
            if label:
                print(f"[{label}] {item}")
            else:
                print(item)
            yield item

    return _inner
