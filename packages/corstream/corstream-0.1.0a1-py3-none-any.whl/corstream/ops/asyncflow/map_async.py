# corstream/ops/asyncflow/map_async.py

from typing import AsyncIterable, AsyncIterator, Callable, TypeVar, Awaitable, Tuple
import asyncio

T = TypeVar("T")
U = TypeVar("U")

AsyncMapFunc = Callable[[T], Awaitable[U]]


def map_async_op(
    fn: AsyncMapFunc[T, U], max_concurrent: int = 5
) -> Callable[[AsyncIterable[T]], AsyncIterable[U]]:
    """
    Applies an async function to items in the stream concurrently,
    with a bounded number of tasks in flight.

    :param fn: An async function to apply to each item.
    :param max_concurrent: The maximum number of concurrent tasks.
    :return: An operator that transforms the async iterable.
    """
    if max_concurrent <= 0:
        raise ValueError("max_concurrent must be >= 1")

    async def _inner(source: AsyncIterable[T]) -> AsyncIterator[U]:
        semaphore = asyncio.Semaphore(max_concurrent)
        queue: asyncio.Queue[Tuple[bool, U | Exception]] = asyncio.Queue()
        tasks = []

        async def worker(item: T) -> None:
            async with semaphore:
                try:
                    result = await fn(item)
                    await queue.put((True, result))
                except Exception as e:
                    await queue.put((False, e))

        async for item in source:
            task = asyncio.create_task(worker(item))
            tasks.append(task)

        # Wait for all tasks to complete
        await asyncio.gather(*tasks)

        # Drain the queue
        while not queue.empty():
            ok, value = await queue.get()
            if ok:
                assert not isinstance(value, Exception)
                yield value
            else:
                raise (
                    value
                    if isinstance(value, Exception)
                    else Exception("Unknown error")
                )

    return _inner
