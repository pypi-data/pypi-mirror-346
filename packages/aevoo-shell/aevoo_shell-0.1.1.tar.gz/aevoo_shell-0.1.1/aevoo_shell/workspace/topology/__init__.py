from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from aevoo_shell.configshell.confignode import ConfigNode
from aevoo_shell.utils.utils import to_bool

if TYPE_CHECKING:
    from aevoo_pycontrol.graphql_client import (
        TopologiesDetails,
        TopologiesDetailsNamespaces,
        TopologyFields,
        TopologyImport,
        Topologies as TopologiesGqlResult,
        Topology as TopologyGqlResult,
        TopologyUpdateTopologyUpdate,
        TopologyDelete,
    )
    from .. import Workspace


@dataclass(eq=False, repr=False)
class NamespaceTopologies(ConfigNode):
    components_name = "Namespaces"

    data: TopologiesDetailsNamespaces = None
    parent = Topologies = None

    def ui_command_rm(self, name: str):
        comp = self.get_child(name)
        if comp is None:
            self.shell.con.raw_write(f"Error: {name} don't exist")
        result: TopologyDelete = self._eval(
            self.ctx.api.topology_delete(comp.cid, self.cid)
        )
        if result.topology_delete:
            self.remove_child(comp)

    def _load(self):
        for component in self.data.list:
            Topology(name=component.cid, parent=self, data=component)


@dataclass(eq=False, repr=False)
class Topologies(ConfigNode):
    components_name = "Topologies"

    data: TopologiesDetails = None
    parent: Workspace = None
    _loaded: bool = False

    def ui_command_import(
        self, url: str, namespace: str | None = None, repo_name: str | None = None
    ):
        result: TopologyImport = self._eval(
            self.ctx.api.topology_import(url, namespace, repo_name=repo_name)
        )
        if result.topology_import:
            self._reload()

    def _load(self):
        for component in self.data.namespaces:
            NamespaceTopologies(name=component.cid, parent=self, data=component)

    def _reload(self):
        result: TopologiesGqlResult = self._eval(self.ctx.api.topologies())
        self.data = result.workspace.topologies
        self._load()


@dataclass(eq=False, repr=False)
class Topology(ConfigNode):
    components_name = "Versions"

    data: TopologyFields = None
    parent: NamespaceTopologies = None

    def summary(self):
        return self.data.stable, self.data.published

    def ui_command_discover(self):
        self._eval(
            self.ctx.api.topology_version_get(cid=self.name, namespace=self.parent.name)
        )

    def ui_command_publish(self, published: bool = True, saas: bool = False):
        result: TopologyUpdateTopologyUpdate = self._eval(
            self.ctx.api.topology_update(
                cid=self.name,
                namespace=self.parent.name,
                published=to_bool(published),
                saas=to_bool(saas),
            ),
            _reload=True,
        )
        self._reload()

    def _load(self):
        for version in self.data.list:
            TopologyVersion(data=version, name=version, parent=self)

    def _reload(self):
        result: TopologyGqlResult = self._eval(
            self.ctx.api.topology(cid=self.name, namespace=self.parent.cid)
        )
        self.data = result.workspace.topologies.find
        # self._load()


class TopologyVersion(ConfigNode):
    pass
