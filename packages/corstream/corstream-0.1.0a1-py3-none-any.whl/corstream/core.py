# corstream/core.py

from __future__ import annotations

from corstream.ops import (
    map_op,
    filter_op,
    batch_op,
    map_async_op,
    log_op,
    catch_op,
    retry_op,
    throttle_op,
)

from corstream.sinks import (
    for_each_sink,
    to_list_sink,
    reduce_sink,
)

from collections.abc import (
    AsyncIterable as AsyncIterableABC,
    Iterable as IterableABC,
)

from typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Callable,
    Generic,
    TypeVar,
    Union,
    List,
    Optional,
)

T = TypeVar("T")
U = TypeVar("U")

Operator = Callable[[AsyncIterable[Any]], AsyncIterable[Any]]


class Stream(Generic[T]):
    """
    Core abstraction representing a lazy, asynchronous data pipeline.

    Stream wraps an asynchronous iterable and allows chained transformation
    operations (like `map`, `filter`, etc.) that are only executed when a
    terminal sink (e.g. `for_each`, `to_list`) is called.
    """

    def __init__(self, source: AsyncIterable[T]):
        self._source: AsyncIterable[T] = source
        self._operations: List[Operator] = []

    def _add_op(self, op: Operator) -> Stream[Any]:
        """
        Internal helper to register a new transformation in the pipeline.
        """
        self._operations.append(op)
        return self

    def apply(self) -> AsyncIterable[Any]:
        """
        Builds the final async iterable by applying all registered operations
        in order. This does not start iteration.
        """
        current = self._source
        for op in self._operations:
            current = op(current)
        return current

    def log(self, label: Optional[str] = None) -> Stream[T]:
        """
        Logs each item in the stream for debugging. Passes items through unchanged.

        :param label: Optional label to prefix each log entry.
        :return: The same stream with logging side effects.
        """
        return self._add_op(log_op(label))

    def catch(self, handler: Callable[[Exception], Optional[T]]) -> Stream[T]:
        """
        Catches exceptions during iteration and applies a handler function.
        The handler can return a replacement value or None to skip the item.

        :param handler: A function that receives the exception and optionally returns a fallback value.
        :return: A new Stream with error handling applied.
        """
        return self._add_op(catch_op(handler))

    def retry(self, retries: int = 3, delay: float = 0.0) -> Stream[T]:
        """
        Adds retry logic to the previous operation in the stream.

        :param retries: Number of times to retry the previous operation on failure.
        :param delay: Optional delay in seconds between retries.
        :return: A new Stream with retry logic applied.
        """
        return self._add_op(retry_op(retries, delay))

    def throttle(self, rate: int, per_seconds: float) -> Stream[T]:
        """
        Throttles the stream to allow only `rate` items per `per_seconds`.

        :param rate: Maximum number of items to process per time window.
        :param per_seconds: Time window in seconds.
        :return: A new Stream with throttling applied.
        """
        return self._add_op(throttle_op(rate, per_seconds))

    def map(self, fn: Callable[[T], Union[U, Awaitable[U]]]) -> "Stream[U]":
        """
        Applies a transformation function to each item in the stream.
        Supports both synchronous and asynchronous functions.

        :param fn: A function to apply to each item.
        :return: A new Stream with transformed output.
        """
        return self._add_op(map_op(fn))

    def map_async(
        self, fn: Callable[[T], Awaitable[U]], max_concurrent: int = 5
    ) -> "Stream[U]":
        """
        Applies an async function to items in the stream concurrently,
        with a controlled concurrency limit.

        :param fn: An async function to map over each item.
        :param max_concurrent: Maximum number of concurrent async calls.
        :return: A new Stream with transformed output.
        """
        return self._add_op(map_async_op(fn, max_concurrent))

    def filter(
        self, predicate: Callable[[T], Union[bool, Awaitable[bool]]]
    ) -> Stream[T]:
        """
        Filters items in the stream using the given predicate function.
        Supports both synchronous and asynchronous predicates.

        :param predicate: A function that returns True to keep the item.
        :return: A Stream containing only items where predicate(item) is True.
        """
        return self._add_op(filter_op(predicate))

    def batch(self, size: int = 1) -> "Stream[List[T]]":
        """
        Groups stream items into batches of fixed size.
        The final batch may contain fewer than `size` items.

        :param size: The number of items per batch. Defaults to 1.
        :return: A Stream of lists, each containing up to `size` items.
        """
        return self._add_op(batch_op(size))

    async def for_each(self, fn: Callable[[T], Union[None, Awaitable[None]]]) -> None:
        """
        Terminal operation that applies a function to each item in the stream.
        This triggers the execution of the pipeline.

        :param fn: A function (sync or async) to call for each item.
        """
        pipeline = self.apply()
        await for_each_sink(pipeline, fn)

    async def to_list(self) -> List[T]:
        """
        Terminal operation that collects all items in the stream into a list.
        This triggers pipeline execution and returns the collected list.

        :return: A list of all output items.
        """
        pipeline = self.apply()
        return await to_list_sink(pipeline)

    async def reduce(self, reducer: Callable[[U, T], U], initial: U) -> U:
        """
        Terminal operation that reduces the stream to a single value using a reducer function.
        This triggers pipeline execution.

        :param reducer: A function of (accumulator, item) -> new acumulator.
        :param initial: The initial value for the accumulator.
        :return: The final reduced value.
        """
        pipeline = self.apply()
        return await reduce_sink(pipeline, reducer, initial)

    @classmethod
    def from_iterable(
        cls, iterable: Union[IterableABC[T], AsyncIterableABC[T]]
    ) -> Stream[T]:
        """
        Creates a stream from either a synchronous iterable (like list, set, range)
        or an asynchronous iterable.

        :param iterable: Any iterable or async iterable source.
        :return: A Stream object wrapping the data source.
        """
        if isinstance(iterable, AsyncIterableABC):  # AsyncIterable
            return cls(iterable)

        if isinstance(iterable, IterableABC):  # Iterable

            async def gen() -> AsyncIterator[T]:
                for item in iterable:
                    yield item

            return cls(gen())

        raise TypeError("Provided input must be an iterable or async iterable.")
