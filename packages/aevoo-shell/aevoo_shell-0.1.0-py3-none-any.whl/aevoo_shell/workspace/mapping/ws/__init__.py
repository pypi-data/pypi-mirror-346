from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from aevoo_shell.configshell.confignode import ConfigNode, print_pretty
from aevoo_shell.workspace.mapping.ws.instance import Instances
from .instance_self import InstancesSelf

if TYPE_CHECKING:
    from .... import Root
    from .. import DomMapping, WssMapping
    from ... import Workspace
    from aevoo_pycontrol.graphql_client import (
        WsMappingDetails,
        MappingsListListWsList,
    )


@dataclass(eq=False, repr=False)
class WsMapping(ConfigNode):
    instances = Instances

    parent: WssMapping
    data: WsMappingDetails = None

    @property
    def dom_mapping(self) -> DomMapping:
        return self.parent.parent

    @property
    def fqdn(self):
        return self.data.fqdn

    def summary(self):
        d = self.data
        s = self.cid
        if d.is_consumer:
            s = "consumer"
            if d.is_provider:
                s += "/provider"
        elif d.is_provider:
            s = "provider"

        return s, d.ready

    def ui_command_info(self):
        print_pretty(self.data, exclude={"instances", "resources"})

    def ui_command_switch(self):
        i = self.data.infos
        if i is None or i.direct_access is not True:
            self.shell.log.error("Permission denied")
        root: Root = self.get_root()
        root.switch(self.dom_mapping.dn, self.dom_mapping.name, self.name)

    def ui_command_update(
        self,
        is_consumer: str = None,
        is_provider: str = None,
        is_saas: str = None,
        # name: str = None,
    ):
        if is_consumer is not None:
            is_consumer = is_consumer.lower() in ("true", "1", "yes")
        if is_provider is not None:
            is_provider = is_provider.lower() in ("true", "1", "yes")
        if is_saas is not None:
            is_saas = is_saas.lower() in ("true", "1", "yes")
        self._eval(
            self.ctx.api.mapping_update(
                self.dom_mapping.dn,
                self.data.cid,
                is_consumer=is_consumer,
                is_provider=is_provider,
                is_saas=is_saas,
                name=self.name,
            ),
            _reload=True,
        )
        self.ui_command_info()

    def _load(self):
        _data = self._eval(self.ctx.api.mapping_get(self.dom_mapping.dn, self.cid))
        self.data = _data.mapping_get
        self.instances(name="instances", parent=self)


@dataclass(eq=False, repr=False)
class WsMappingSelf(WsMapping):
    instances = InstancesSelf

    parent: Workspace
    data: MappingsListListWsList = None
