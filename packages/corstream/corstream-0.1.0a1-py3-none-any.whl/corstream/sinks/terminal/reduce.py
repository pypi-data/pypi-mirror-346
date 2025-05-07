# corstream/sinks/terminal/reduce.py

from typing import AsyncIterable, Callable, TypeVar

T = TypeVar("T")
U = TypeVar("U")


async def reduce_sink(
    source: AsyncIterable[T], reducer: Callable[[U, T], U], initial: U
) -> U:
    """
    Terminal sink that reduces the stream to a single value using a reducer function.

    :param source: The async iterable to consume.
    :param reducer: A function that takes (accumulator, item) and returns a new accumulator.
    :param initial: The initial value for the accumulator.
    :return: Final reduced value.
    """
    acc = initial
    async for item in source:
        acc = reducer(acc, item)
    return acc
