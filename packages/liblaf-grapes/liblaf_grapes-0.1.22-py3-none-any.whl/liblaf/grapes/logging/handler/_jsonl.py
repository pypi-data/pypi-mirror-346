from pathlib import Path
from typing import Unpack

import loguru
from environs import env

from liblaf.grapes.logging.filters import Filter, make_filter
from liblaf.grapes.typed import PathLike


def jsonl_handler(
    file: PathLike | None = None,
    filter_: Filter | None = None,
    **kwargs: Unpack["loguru.FileHandlerConfig"],
) -> "loguru.HandlerConfig":
    if file is None:
        file = env.path("LOGGING_JSONL", default=Path("run.log.jsonl"))
    filter_ = make_filter(filter_)
    return {"sink": file, "filter": filter_, "serialize": True, "mode": "w", **kwargs}
