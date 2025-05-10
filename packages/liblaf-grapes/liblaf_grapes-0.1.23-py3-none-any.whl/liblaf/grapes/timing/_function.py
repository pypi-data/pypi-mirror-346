import functools
from collections.abc import Callable, Sequence

from liblaf.grapes import pretty

from . import callback
from ._base import Callback, TimerRecords


class TimedFunction[**P, T]:
    timing: TimerRecords
    _func: Callable[P, T]

    def __init__(
        self,
        func: Callable[P, T],
        /,
        name: str | None = None,
        timers: Sequence[str] = ("perf",),
        callback_start: Callback | None = None,
        callback_stop: Callback | None = None,
        callback_finally: Callback | None = None,
    ) -> None:
        if name is None:
            name = pretty.func(func).plain or "Function"
        if callback_stop is None:
            callback_stop = callback.log_record(depth=3)
        self.timing = TimerRecords(
            name=name,
            timers=timers,
            callback_start=callback_start,
            callback_stop=callback_stop,
            callback_finally=callback_finally,
        )
        self._func = func
        functools.update_wrapper(self, func)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        self.timing._start()  # noqa: SLF001
        result: T = self._func(*args, **kwargs)
        self.timing._stop()  # noqa: SLF001
        return result
