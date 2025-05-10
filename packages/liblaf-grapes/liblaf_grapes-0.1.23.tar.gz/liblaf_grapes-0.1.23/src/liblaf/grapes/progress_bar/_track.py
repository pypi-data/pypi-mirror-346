from collections.abc import Generator, Iterable, Sequence

from rich.progress import Progress

from liblaf.grapes import timing

from ._progress import progress


def track[T](
    iterable: Iterable[T],
    *,
    description: str = "Progress",
    timers: bool | Sequence[timing.TimerName | str] = ["perf"],
    total: float | None = None,
    callback_start: timing.Callback | None = None,
    callback_stop: timing.Callback | None = None,
    callback_finally: timing.Callback | None = None,
) -> Generator[T]:
    prog: Progress = progress()
    if timers is True:
        timers = ["perf"]
    if total is None:
        total = try_len(iterable)
    if timers:
        if callback_stop is None:
            callback_stop = timing.callback.log_record(depth=5)
        if callback_finally is None:
            callback_finally = timing.callback.log_summary(depth=5)
        iterable: timing.TimedIterable[T] = timing.timer(
            iterable,
            name=description,
            timers=timers,
            total=int(total) if total is not None else None,
            callback_start=callback_start,
            callback_stop=callback_stop,
            callback_finally=callback_finally,
        )
        with prog:
            yield from prog.track(iterable, total=total, description=description)
    else:
        with prog:
            yield from prog.track(iterable, total=total, description=description)


def try_len(iterable: Iterable) -> int | None:
    try:
        return len(iterable)  # pyright: ignore[reportArgumentType]
    except TypeError:
        return None
