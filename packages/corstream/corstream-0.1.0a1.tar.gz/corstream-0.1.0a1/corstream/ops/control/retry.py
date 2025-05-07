# corstream/ops/control/retry.py

from typing import AsyncIterable, AsyncIterator, Callable, TypeVar
import asyncio

T = TypeVar("T")


def retry_op(
    retries: int = 3, delay: float = 0.0
) -> Callable[[AsyncIterable[T]], AsyncIterable[T]]:
    """
    Wraps the previous operator in the stream with retry logic.
    Retries the item up to `retries` times with optional delay between attempts.

    :param retries: Number of retries before giving up.
    :param delay: Delay in seconds between retries.
    :return: A retry-enabled async iterable.
    """

    async def _inner(source: AsyncIterable[T]) -> AsyncIterator[T]:
        async for item in source:
            attempt = 0
            while True:
                try:
                    yield item
                    break  # Success
                except Exception:
                    attempt += 1
                    if attempt > retries:
                        raise
                    if delay > 0:
                        await asyncio.sleep(delay)

    return _inner
