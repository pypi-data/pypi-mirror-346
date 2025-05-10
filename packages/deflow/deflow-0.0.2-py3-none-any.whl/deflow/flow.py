# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from datetime import datetime
from typing import Optional

from ddeutil.workflow import Result, Workflow
from ddeutil.workflow import config as workflow_config

from .__types import DictData
from .conf import ASSETS_PATH, config


def workflow_factory(
    name: str,
    version: str,
    *,
    extras: Optional[DictData] = None,
) -> Workflow:
    """Routing workflow function.

    :param name: (str) A name of data pipeline.
    :param version: (str) A version of data framework.
    :param extras: An extra parameter that want to override core config values.

    :rtype: Workflow
    """
    extras: DictData = {
        **{
            "conf_path": ASSETS_PATH / f"{config.version}/templates",
            "registry_caller": [
                f"deflow.assets.{config.version}.core",
                *extras.pop("registry_caller", []),
            ],
            "conf_paths": [config.conf_path],
        },
        **(extras or {}),
    }
    if version == "v1":
        return Workflow.from_conf(
            name="stream-workflow",
            extras=extras
            | {
                "audit_path": workflow_config.audit_path / f"stream={name}",
            },
        )
    raise NotImplementedError(f"Flow version: {version!r} does not implement.")


class Flow:
    """Flow object for manage workflow model release and test via configuration.
    This is the core object for this package that active data pipeline from
    the current data framework version.

    :param name: (str) A stream name.
    :param version: (str) A version of data framework.
    :param extras: (DictData) An extra parameters that want to override the
        workflow config.
    """

    def __init__(
        self,
        name: str,
        *,
        version: Optional[str] = None,
        extras: Optional[DictData] = None,
    ) -> None:
        self.name: str = name
        self.version: str = version or config.version
        self.extras: DictData = extras or {}
        self.workflow: Workflow = workflow_factory(
            name, version=self.version, extras=self.extras
        )

    def __repr__(self) -> str:
        """Override __repr__ method.

        :rtype: str
        """
        return f"{self.__class__.__name__}(name={self.name})"

    def __str__(self) -> str:
        """Override __str__ method.

        :rtype: str
        """
        return self.name

    def run(self, mode: str) -> Result:
        """Start release dynamic pipeline with this flow name.

        :param mode: (str) A running mode of this flow.

        :result: Result
        """
        return self.workflow.release(
            release=datetime.now(),
            params={
                "name": self.name,
                "run-mode": mode,
            },
        )

    def test(self) -> Result:
        """Test running flow on local without integration testing.

        :result: Result
        """
        return self.run(mode="TEST")

    def ui(self): ...
