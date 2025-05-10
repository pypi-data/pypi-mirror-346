# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from datetime import datetime
from functools import partial

from ddeutil.workflow import Result, tag

from ....__types import DictData
from ....conf import config
from .models import Frequency, Process, Stream

VERSION: str = "v1"
tag_v1 = partial(tag, name=VERSION)


@tag_v1(alias="get-stream-info")
def get_stream_info(name: str, result: Result) -> DictData:
    """Get Stream model information. This function use to validate an input
    stream name that exists on the config path.

    :param name: (str) A stream name
    :param result: (Result) A result dataclass for make logging.

    :rtype: DictData
    """
    result.trace.info(f"[CALLER]: Start getting stream: {name!r} info.")
    stream: Stream = Stream.from_path(name=name, path=config.conf_path)
    return {
        "name": stream.name,
        "freq": stream.freq.model_dump(by_alias=True),
        "data_freq": stream.data_freq.model_dump(by_alias=True),
        "priority-groups": sorted(stream.priority_group().keys()),
        "stream": stream,
    }


@tag_v1(alias="start-stream")
def start_stream(
    name: str, freq: Frequency, data_freq: Frequency, result: Result
) -> DictData:
    """Start stream workflow with update audit watermarking and generate starter
    stream log.

    :param name: (str) A stream name that want to get audit logs for generate
        the next audit date.
    :param freq: (Frequency) A audit date frequency.
    :param data_freq: (Frequency) A logical date frequency.
    :param result: (Result) A result dataclass for make logging.
    """
    result.trace.info(f"[CALLER]: Start running stream: {name!r}.")
    result.trace.info(f"[CALLER]: ... freq: {freq}")
    result.trace.info(f"[CALLER]: ... data_freq: {data_freq}")
    return {
        "audit-date": datetime(2025, 4, 1, 1),
        "logical-date": datetime(2025, 4, 1, 1),
    }


@tag_v1(alias="get-groups-from-priority")
def get_groups_from_priority(
    priority: int, stream: str, result: Result
) -> DictData:
    """Get groups from priority.

    :param priority: (int)
    :param stream: (str)
    :param result: (Result)
    """
    result.trace.info(f"[CALLER]: Get groups from priority: {priority}")
    stream: Stream = Stream.from_path(name=stream, path=config.conf_path)
    priority_group = stream.priority_group()
    result.trace.info(f"[CALLER]: ... Return groups from {priority}")
    return {"groups": [group.name for group in priority_group.get(priority)]}


@tag_v1(alias="get-processes-from-group")
def get_processes_from_group(
    group: str, stream: str, result: Result
) -> DictData:
    result.trace.info(f"[CALLER]: Get processes from group: {group!r}")
    stream: Stream = Stream.from_path(name=stream, path=config.conf_path)
    return {"processes": list(stream.group(group).processes)}


@tag_v1(alias="start-process")
def start_process(name: str, result: Result) -> DictData:
    """Start process with an input process name."""
    result.trace.info(f"[CALLER]: Start process: {name!r}")
    process: Process = Process.from_path(name=name, path=config.conf_path)
    return {
        "routing": process.routing,
        "process": process.model_dump(by_alias=True),
    }
