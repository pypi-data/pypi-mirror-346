import collections
import statistics
import textwrap
from collections.abc import Callable, Generator, Mapping, Sequence
from typing import overload, override

import attrs
from loguru import logger

from liblaf.grapes import human

from ._time import get_time


@attrs.define
class SingleTimer:
    name: str | None = attrs.field(default=None, kw_only=True)
    timers: Sequence[str] = attrs.field(default=("perf",), kw_only=True)
    _time_start: dict[str, float] = attrs.field(init=False, factory=dict)
    _time_stop: dict[str, float] = attrs.field(init=False, factory=dict)

    @property
    def default_timer(self) -> str:
        return self.timers[0]

    @property
    def _current_record(self) -> Mapping[str, float]:
        return {timer: self.elapsed(timer) for timer in self.timers}

    def elapsed(self, timer: str | None = None) -> float:
        if timer is None:
            timer = self.default_timer
        if timer in self._time_stop:
            return self._time_stop[timer] - self._time_start[timer]
        return get_time(timer) - self._time_start[timer]

    def _start(self) -> None:
        for timer in self.timers:
            self._time_start[timer] = get_time(timer)
        self._time_stop.clear()

    def _stop(self) -> None:
        for timer in self.timers:
            self._time_stop[timer] = get_time(timer)


class NoOpType: ...


NOOP = NoOpType()

type Callback = Callable[["TimerRecords"], None] | NoOpType


@attrs.define
class TimerRecords(SingleTimer):
    _records: dict[str, list[float]] = attrs.field(
        init=False, factory=lambda: collections.defaultdict(list)
    )
    callback_start: Callback | None = attrs.field(default=None, kw_only=True)
    callback_stop: Callback | None = attrs.field(default=None, kw_only=True)
    callback_finally: Callback | None = attrs.field(default=None, kw_only=True)

    @overload
    def __getitem__(self, key: int) -> Mapping[str, float]: ...
    @overload
    def __getitem__(self, key: str) -> Sequence[float]: ...
    def __getitem__(self, key: int | str) -> Mapping[str, float] | Sequence[float]:
        if isinstance(key, int):
            return {k: v[key] for k, v in self._records.items()}
        if isinstance(key, str):
            return self._records[key]
        raise KeyError(key)

    def __len__(self) -> int:
        return len(self._records[self.default_timer])

    @property
    def columns(self) -> Sequence[str]:
        return self.timers

    @property
    def count(self) -> int:
        return self.n_rows

    @property
    def n_columns(self) -> int:
        return len(self.timers)

    @property
    def n_rows(self) -> int:
        return len(self.column())

    def column(self, timer: str | None = None) -> Sequence[float]:
        if timer is None:
            timer = self.default_timer
        return self._records[timer]

    def human_record(self, index: int = -1) -> str:
        return human_record(self.row(index), name=self.name)

    def human_summary(self) -> str:
        name: str = self.name or "Timer"
        header: str = f"{name} (total: {self.n_rows})"
        if self.n_rows == 0:
            return header
        body: str = ""
        for timer in self.columns:
            body += f"{timer} > "
            human_mean: str = human.human_duration_series(self.column(timer))
            human_median: str = human.human_duration(self.median(timer))
            body += f"mean: {human_mean}, median: {human_median}\n"
        body = body.strip()
        summary: str = header + "\n" + textwrap.indent(body, "    ")
        return summary

    def iter_columns(self) -> Generator[tuple[str, Sequence[float]]]:
        yield from self._records.items()

    def iter_rows(self) -> Generator[Mapping[str, float]]:
        for index in range(self.n_rows):
            yield self.row(index)

    def log_record(
        self, index: int = -1, depth: int = 1, level: int | str = "DEBUG"
    ) -> None:
        logger.opt(depth=depth).log(level, self.human_record(index=index))

    def log_summary(self, depth: int = 1, level: int | str = "INFO") -> None:
        logger.opt(depth=depth).log(level, self.human_summary())

    def row(self, index: int) -> Mapping[str, float]:
        return {timer: values[index] for timer, values in self._records.items()}

    # region statistics

    def max(self, timer: str | None = None) -> float:
        return max(self.column(timer))

    def mean(self, timer: str | None = None) -> float:
        return statistics.mean(self.column(timer))

    def median(self, timer: str | None = None) -> float:
        return statistics.median(self.column(timer))

    def min(self, timer: str | None = None) -> float:
        return min(self.column(timer))

    def std(self, timer: str | None = None) -> float:
        return statistics.stdev(self.column(timer))

    # endregion statistics

    def _append(
        self, seconds: Mapping[str, float] = {}, nanoseconds: Mapping[str, float] = {}
    ) -> None:
        for key, value in seconds.items():
            self._records[key].append(value)
        for key, value in nanoseconds.items():
            self._records[key].append(value * 1e-9)

    @override
    def _start(self) -> None:
        if callable(self.callback_start):
            self.callback_start(self)
        super()._start()

    @override
    def _stop(self) -> None:
        super()._stop()
        self._append(seconds=self._current_record)
        if callable(self.callback_stop):
            self.callback_stop(self)

    def _finally(self) -> None:
        if callable(self.callback_finally):
            self.callback_finally(self)


def human_record(record: Mapping[str, float], name: str | None = None) -> str:
    name = name or "Timer"
    text: str = f"{name} > "
    items: list[str] = []
    for timer, value in record.items():
        human_duration: str = human.human_duration(value)
        items.append(f"{timer}: {human_duration}")
    text += ", ".join(items)
    return text


def human_summary(records: Mapping[str, Sequence[float]], name: str | None) -> str:
    name = name or "Timer"
    header: str = f"{name} (total: {len(records)})"
    if len(records) == 0:
        return header
    body: str = ""
    for timer, values in records.items():
        body += f"{timer} > "
        human_mean: str = human.human_duration_series(values)
        human_median: str = human.human_duration(statistics.median(values))
        body += f"mean: {human_mean}, median: {human_median}\n"
    body = body.strip()
    summary: str = header + "\n" + textwrap.indent(body, "    ")
    return summary
