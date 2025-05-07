# corstream/ops/batch.py

from typing import AsyncIterable, AsyncIterator, Callable, List, TypeVar

T = TypeVar("T")


def batch_op(size: int = 1) -> Callable[[AsyncIterable[T]], AsyncIterable[List[T]]]:
    """
    Creates a batching operator that groups items into fixed-size lists.

    :param size: The number of items per batch. Defaults to 1.
    :return: A transformation function to apply to an AsyncIterable.
    """
    if size <= 0:
        raise ValueError("Batch size must be a positive integer.")

    async def _inner(source: AsyncIterable[T]) -> AsyncIterator[List[T]]:
        batch: List[T] = []
        async for item in source:
            batch.append(item)
            if len(batch) == size:
                yield batch
                batch = []
        if batch:
            yield batch

    return _inner
