from __future__ import annotations

from typing import TYPE_CHECKING

from aevoo_shell.configshell.confignode import ConfigNode
from .instance import instances_load
from .service import services_load

if TYPE_CHECKING:
    from aevoo_shell import Root


def marketplace_load(parent: Root):
    marketplace = ConfigNode(name="marketplace", parent=parent)
    services_load(marketplace)
    instances_load(marketplace)
