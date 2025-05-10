import contextlib
import enum
import types
from collections.abc import Callable, Iterable, Sequence
from typing import Self, overload

import attrs

from liblaf.grapes.timing import callback

from ._base import Callback, TimerRecords
from ._function import TimedFunction
from ._iterable import TimedIterable


class TimerMode(enum.StrEnum):
    CONTEXT_MANAGER = "context-manager"
    FUNCTION = "function"
    ITERABLE = "iterable"
    INLINE = "inline"


@attrs.define
class Timer(
    contextlib.AbstractAsyncContextManager,
    contextlib.AbstractContextManager,
    TimerRecords,
):
    _mode: TimerMode | None = None

    async def __aenter__(self) -> Self:
        self.mode = TimerMode.CONTEXT_MANAGER
        self._start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        self._stop()

    @overload
    def __call__[**P, T](self, func: Callable[P, T], /) -> TimedFunction[P, T]: ...
    @overload
    def __call__[T](
        self, iterable: Iterable[T], /, *, total: int | None = None
    ) -> TimedIterable[T]: ...
    def __call__(
        self, func_or_iterable: Callable | Iterable, /, *, total: int | None = None
    ) -> TimedFunction | TimedIterable:
        if callable(func_or_iterable):
            return TimedFunction(
                func_or_iterable,
                name=self.name,
                timers=self.timers,
                callback_start=self.callback_start,
                callback_stop=self.callback_stop,
                callback_finally=self.callback_finally,
            )
        # if isinstance(func_or_iterable, Iterable):
        return TimedIterable(
            func_or_iterable,
            name=self.name,
            timers=self.timers,
            total=total,
            callback_start=self.callback_start,
            callback_stop=self.callback_stop,
            callback_finally=self.callback_finally,
        )

    def __enter__(self) -> Self:
        self.mode = TimerMode.CONTEXT_MANAGER
        self._start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        self._stop()

    @property
    def mode(self) -> TimerMode | None:
        return self._mode

    @mode.setter
    def mode(self, value: TimerMode) -> None:
        if self._mode == value:
            return
        self._mode = value
        match value:
            case TimerMode.CONTEXT_MANAGER:
                if self.name is None:
                    self.name = "Block"
                if self.callback_stop is None:
                    self.callback_stop = callback.log_record(depth=3)
            case TimerMode.INLINE:
                if self.callback_stop is None:
                    self.callback_stop = callback.log_record(depth=3)
            case _:
                pass

    def start(self) -> None:
        self.mode = TimerMode.INLINE
        self._start()

    def stop(self) -> None:
        self._stop()


@overload
def timer[T](
    iterable: Iterable[T],
    /,
    *,
    name: str = "Iterable",
    timers: Sequence[str] = ("perf",),
    total: int | None = None,
    callback_start: Callback | None = None,
    callback_stop: Callback | None = None,
    callback_finally: Callback | None = None,
) -> TimedIterable[T]: ...
@overload
def timer[**P, T](
    func: Callable[P, T],
    /,
    *,
    name: str | None = None,
    timers: Sequence[str] = ("perf",),
    callback_start: Callback | None = None,
    callback_stop: Callback | None = None,
    callback_finally: Callback | None = None,
) -> TimedFunction[P, T]: ...
@overload
def timer(
    *,
    name: str | None = None,
    timers: Sequence[str] = ("perf",),
    callback_start: Callback | None = None,
    callback_stop: Callback | None = None,
    callback_finally: Callback | None = None,
) -> Timer: ...
def timer(
    func_or_iterable: Callable | Iterable | None = None,
    /,
    *,
    name: str | None = None,
    timers: Sequence[str] = ("perf",),
    total: int | None = None,
    callback_start: Callback | None = None,
    callback_stop: Callback | None = None,
    callback_finally: Callback | None = None,
) -> TimedFunction | TimedIterable | Timer:
    timer = Timer(
        name=name,
        timers=timers,
        callback_start=callback_start,
        callback_stop=callback_stop,
        callback_finally=callback_finally,
    )
    if func_or_iterable is None:
        return timer
    if callable(func_or_iterable):
        return timer(func_or_iterable)
    # if isinstance(func_or_iterable, Iterable):
    return timer(func_or_iterable, total=total)
