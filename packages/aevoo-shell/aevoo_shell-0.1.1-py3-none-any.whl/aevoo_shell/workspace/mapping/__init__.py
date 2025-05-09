from __future__ import annotations

from dataclasses import dataclass
from pprint import pprint
from typing import TYPE_CHECKING

from aevoo_shell.configshell.confignode import ConfigNode
from aevoo_shell.workspace.mapping.ws.instance import Instances
from .ws import WsMapping

if TYPE_CHECKING:
    from aevoo_pycontrol.graphql_client import (
        MappingsListList,
        MappingsListListWsList,
    )
    from .. import Workspace


@dataclass(eq=False, repr=False)
class Mappings(ConfigNode):
    data: list[MappingsListList] = None
    parent: Workspace = None
    _loaded: bool = False

    def _load(self):
        for d in self.data:
            DomMapping(dn=d.cid, name=d.name, parent=self, data=d)


@dataclass(eq=False, repr=False)
class DomMapping(ConfigNode):
    data: MappingsListList = None
    dn: str = None

    def ui_command_info(self):
        pprint(self.data)

    def _load(self):
        WssMapping(data=self.data.ws_list, name="workspaces", parent=self)


@dataclass(eq=False, repr=False)
class WssMapping(ConfigNode):
    parent: DomMapping
    data: list[MappingsListListWsList] = None

    def _load(self):
        for ws_ in self.data:
            WsMapping(data=ws_, name=ws_.cid, parent=self)
