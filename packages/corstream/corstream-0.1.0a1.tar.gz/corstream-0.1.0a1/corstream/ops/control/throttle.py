# corstream/ops/control/throttle.py

from typing import AsyncIterable, AsyncIterator, Callable, TypeVar
import asyncio
import time

T = TypeVar("T")


def throttle_op(
    rate: int, per_seconds: float
) -> Callable[[AsyncIterable[T]], AsyncIterable[T]]:
    """
    Limits the flow of items to a maximum of `rate` items per `per_seconds` seconds.

    :param rate: The maximum number of items to emit.
    :param per_seconds: The time window in seconds for the rate limit.
    :return: Throttled async iterable.
    """
    if rate <= 0 or per_seconds <= 0:
        raise ValueError("Rate and per_seconds must be positive values.")

    interval = per_seconds / rate

    async def _inner(source: AsyncIterable[T]) -> AsyncIterator[T]:
        last_emit = 0.0
        async for item in source:
            now = time.perf_counter()
            wait_time = last_emit + interval - now
            if wait_time > 0:
                await asyncio.sleep(wait_time)
            last_emit = time.perf_counter()
            yield item

    return _inner
