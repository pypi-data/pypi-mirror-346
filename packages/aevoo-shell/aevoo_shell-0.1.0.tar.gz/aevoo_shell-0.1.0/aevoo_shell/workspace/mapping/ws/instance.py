from __future__ import annotations

import json
from dataclasses import dataclass
from getpass import getpass
from typing import TYPE_CHECKING

from aevoo_shell.configshell.confignode import ConfigNode
from aevoo_shell.utils.instance import secret_write_to
from aevoo_shell.utils.utils import confirm

if TYPE_CHECKING:
    from aevoo_shell.workspace import WsMapping
    from aevoo_pycontrol.graphql_client import (
        InstancesListInstancesList,
    )


@dataclass(eq=False, repr=False)
class Instances(ConfigNode):
    ls_reload = True

    data: list[InstancesListInstancesList] = None
    parent: WsMapping = None
    _loaded: bool = False

    @property
    def domain_dn(self):
        return self.parent.parent.parent.data.cid4

    @property
    def mapping_id(self):
        return self.parent.data.cid

    def ui_command_create(
        self,
        cid: str,
        model_name: str,
        domain_dn: str | None,
        mapping_id: str | None,
        inputs: str | None = None,
        model_ns: str = "default",
        version: str = None,
    ):
        if inputs is not None:
            inputs = json.loads(inputs)
        self._eval(
            self.ctx.api.instance_create(
                cid, model_name, domain_dn, mapping_id, inputs, model_ns, version
            ),
            _reload=True,
        )

    def ui_command_rm(self, instance: str):
        if confirm("Delete instance ? "):
            self._eval(
                self.ctx.api.instance_delete(instance, self.domain_dn, self.mapping_id)
            )

    def ui_complete_rm(self, parameters: dict[str, str], text: str, current_param: str):
        return [i.name for i in self.children if text == "" or i.name.startswith(text)]

    def _load(self):
        self.data = self._eval(
            self.ctx.api.instances_list(
                domain_dn=self.domain_dn, mapping_id=self.mapping_id
            )
        ).instances_list
        for component in self.data:
            Instance(name=component.cid, parent=self, data=component)


@dataclass(eq=False, repr=False)
class Instance(ConfigNode):
    data: InstancesListInstancesList = None
    parent: Instances = None

    def summary(self):
        d = self.data
        return f"({d.topology}) {d.status}", d.status == "started"

    def ui_command_info(self):
        print(json.dumps(self.data.model_dump(), indent=2))

    def ui_command_secret_write_to(self, secret_name: str, file: str):
        api = self.ctx.api
        fqdn = self.parent.parent.fqdn
        cid = self.data.cid
        pwd = getpass()
        _secret_ = self._eval(
            api.instance_secret_get(fqdn, cid, pwd, secret_name)
        ).instance_secret_get
        secret_write_to(
            self.data.secrets.get(secret_name),
            _secret_,
            file,
        )
