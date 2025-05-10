import functools

from loguru import logger

from ._base import NOOP, Callback, TimerRecords


def log_record(index: int = -1, depth: int = 1, level: int | str = "DEBUG") -> Callback:
    return functools.partial(_log_record, index=index, depth=depth, level=level)


def log_summary(depth: int = 1, level: int | str = "INFO") -> Callback:
    return functools.partial(_log_summary, depth=depth, level=level)


def _log_record(
    timer: TimerRecords, *, index: int = -1, depth: int = 1, level: int | str = "DEBUG"
) -> None:
    logger.opt(depth=depth).log(level, timer.human_record(index=index))


def _log_summary(
    timer: TimerRecords, *, depth: int = 1, level: int | str = "INFO"
) -> None:
    logger.opt(depth=depth).log(level, timer.human_summary())


__all__ = ["NOOP", "log_record", "log_summary"]
