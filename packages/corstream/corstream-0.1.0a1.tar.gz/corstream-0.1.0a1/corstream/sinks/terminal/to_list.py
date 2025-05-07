# corstream/sinks/terminal/to_list.py

from typing import AsyncIterable, TypeVar, List

T = TypeVar("T")


async def to_list_sink(source: AsyncIterable[T]) -> List[T]:
    """
    Terminal sink that collects all items from the stream into a list.

    :param source: The async iterable to consume.
    :return: A list of all stream items.
    """
    result: List[T] = []
    async for item in source:
        result.append(item)
    return result
