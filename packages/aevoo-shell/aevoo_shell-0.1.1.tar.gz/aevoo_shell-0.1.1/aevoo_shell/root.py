from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from aevoo_shell.configshell.confignode import ConfigNode
from .marketplace import marketplace_load
from .workspace import Domain, Workspace

if TYPE_CHECKING:
    pass


@dataclass(eq=False, repr=False)
class Root(ConfigNode):
    domains: ConfigNode = None
    children: set[Domain] = field(init=False)

    def switch(self, domain_dn: str, domain_name: str, ws_name: str):
        for d in self.children:
            if d.dn == domain_dn:
                domain = d
                break
        else:
            domain = Domain(dn=domain_dn, name=domain_name, parent=self.domains)
        for ws in domain.children:
            if ws.name == ws_name:
                break
        else:
            Workspace(name=ws_name, parent=domain)
        self.shell.run_cmdline(f"cd /domains/{domain_name}/{ws_name}")

    def ui_command_switch(self, domain_dn: str, domain_name: str, ws_name: str):
        if not self.domains.exist(domain_name):
            domain = Domain(dn=domain_dn, name=domain_name, parent=self.domains)
            if not domain.exist(ws_name):
                Workspace(name=ws_name, parent=domain)
        self.shell.run_cmdline(f"cd /domains/{domain_name}")
        self.shell.run_cmdline(f"cd {ws_name}")

    def ui_command_token_create(self):
        self._eval(self.ctx.api.token_reset())

    def _load(self):
        self.domains_load()
        marketplace_load(self)

    def domains_load(self):
        self.domains = ConfigNode(name="domains", parent=self)
        _activity = self._eval(self.ctx.api.user_activity()).user_activity
        for a in _activity:
            if not self.domains.exist(a.name):
                d = Domain(dn=a.dn, name=a.name, parent=self.domains, ws_act=a.ws_act)
