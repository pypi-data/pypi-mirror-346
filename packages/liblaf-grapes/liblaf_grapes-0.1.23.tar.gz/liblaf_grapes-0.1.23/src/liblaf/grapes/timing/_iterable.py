from collections.abc import Iterable, Iterator, Sequence

from . import callback
from ._base import Callback, TimerRecords


class TimedIterable[T]:
    timing: TimerRecords
    _iterable: Iterable[T]
    _total: int | None = None

    def __init__(
        self,
        iterable: Iterable[T],
        /,
        total: int | None = None,
        name: str | None = None,
        timers: Sequence[str] = ("perf",),
        callback_start: Callback | None = None,
        callback_stop: Callback | None = None,
        callback_finally: Callback | None = None,
    ) -> None:
        if name is None:
            name = "Iterable"
        if callback_stop is None:
            callback_stop = callback.log_record(depth=3)
        if callback_finally is None:
            callback_finally = callback.log_summary(depth=3)
        self.timing = TimerRecords(
            name=name,
            timers=timers,
            callback_start=callback_start,
            callback_stop=callback_stop,
            callback_finally=callback_finally,
        )
        self._iterable = iterable
        self._total = total

    def __contains__(self, x: object, /) -> bool:
        return x in self._iterable  # pyright: ignore[reportOperatorIssue]

    def __len__(self) -> int:
        if self._total is None:
            return len(self._iterable)  # pyright: ignore[reportArgumentType]
        return self._total

    def __iter__(self) -> Iterator[T]:
        for item in self._iterable:
            self.timing._start()  # noqa: SLF001
            yield item
            self.timing._stop()  # noqa: SLF001
        self.timing._finally()  # noqa: SLF001
