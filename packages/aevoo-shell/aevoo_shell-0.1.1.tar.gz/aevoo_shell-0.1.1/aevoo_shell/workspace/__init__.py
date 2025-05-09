from __future__ import annotations

from dataclasses import dataclass, field
from pprint import pprint
from typing import TYPE_CHECKING

from aevoo_shell.configshell.confignode import ConfigNode
from .credential import Credentials
from .mapping import Mappings, WsMapping
from .mapping.ws import WsMappingSelf
from .topology import Topologies

if TYPE_CHECKING:
    from aevoo_pycontrol.graphql_client import (
        MappingsListList,
        UserActivityUserActivityWsAct,
        MappingsListListWsList,
        WorkspaceMinWorkspace,
    )


@dataclass(eq=False, repr=False)
class Domain(ConfigNode):
    children: set[Workspace] = field(init=False)
    dn: str = None
    ws_act: list[UserActivityUserActivityWsAct] = field(default_factory=list)

    def _load(self):
        for a in self.ws_act:
            name = a.id
            if not self.exist(name):
                Workspace(name=name, parent=self)

    def summary(self):
        return f"domain ({self.dn})", True


@dataclass(eq=False, repr=False)
class Workspace(ConfigNode):
    parent: Domain

    # auth_dn: str = None
    data: WorkspaceMinWorkspace = None

    def ui_command_info(self):
        if self.data:
            return pprint(self.data.metas)

    def _load(self):
        if self.loaded is False:
            dom: Domain
            for dom in self.parent.parent.children:
                for ws in dom.children:
                    ws.loaded = False
            # request = self.ctx.switch(self.parent.dn, self.name, self.auth_dn)
            request = self.ctx.switch(self.parent.dn, self.name)
            result = self._eval(request)
            if result is None:
                self.shell.con.raw_write(f"Failed to load token env\n")
                self.shell.run_cmdline("cd /")
                return
            ok, token = result
            if ok is False:
                self.shell.con.raw_write(f"Failed to load token env\n")
                self.shell.run_cmdline("cd /")
                return
        if self.ctx.user_ctx.profile is not None:
            Credentials(name="credentials", parent=self)
            self.data = self._eval(self.ctx.api.workspace_min()).workspace
            _mappings_list = self.data.mappings.list
            _self_mapping: MappingsListListWsList | None = None
            m: MappingsListList
            for m in _mappings_list:
                if m.cid == self.parent.dn:
                    for i, ws_m in enumerate(m.ws_list):
                        if ws_m.cid == self.ctx.user_ctx.ws_cid:
                            _self_mapping = ws_m
                            m.ws_list.pop(i)
                            break
                    else:
                        raise Exception("Self mapping not found")
            WsMappingSelf(name="self_mapping", parent=self, data=_self_mapping)
            Mappings(name="mappings", parent=self, data=_mappings_list)
            Topologies(name="topologies", parent=self, data=self.data.topologies)

    def summary(self):
        return "workspace", True
