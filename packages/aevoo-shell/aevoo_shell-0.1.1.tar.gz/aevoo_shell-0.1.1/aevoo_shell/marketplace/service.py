from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

from aevoo_shell.configshell.confignode import ConfigNode
from aevoo_shell.utils import async_run
from aevoo_tosca.v2.properties_attributes_parameters.property import (
    PropertyDefinition,
)

if TYPE_CHECKING:
    from aevoo_pycontrol.graphql_client import (
        SaasSaasServices,
        ServiceDetailsFragment,
        SaasSaas,
    )


def services_load(parent: ConfigNode):
    services = ConfigNode(name="services", parent=parent)
    _services = async_run(services.ctx.api.saas()).saas
    for _service in _services:
        ws = Services(data=_service, name=_service.fqdn, parent=services)
        for s in _service.services:
            service = Service(data=s, name=s.cid, parent=ws)


@dataclass(eq=False, repr=False)
class Services(ConfigNode):
    data: SaasSaas = None


@dataclass(eq=False, repr=False)
class Service(ConfigNode):
    data: SaasSaasServices = None
    details: ServiceDetailsFragment = None
    parent: Services = None

    @property
    def fqdn(self):
        return self.parent.name

    def ui_command_info(self):
        print(json.dumps(self.details.inputs, indent=4))

    def ui_command_instance_create(self, name: str, **kwargs):
        inputs = {}
        for _input, _details in self.details.inputs.items():
            _info = PropertyDefinition(**_details)
            _value = kwargs.get(_input)
            if _value is None:
                if _input == "name":
                    _value = name
                else:
                    _value = input(f"Value for '{_input}' : ")
            match _info.type:
                case "integer":
                    _value = int(_value)
                    break
            inputs[_input] = _value

        _kwargs = dict(
            inputs=inputs,
            model=self.data.cid,
            target=self.fqdn,
            time_unit="per_month",
        )

        eval_price = self._eval(self.ctx.api.saas_price(**_kwargs))
        price = eval_price.saas_price
        print(name, price, _kwargs)

        self._eval(
            self.ctx.api.saas_transaction_create(name=name, price=price, **_kwargs),
            _reload=True,
        )

    def __post_init__(self):
        super().__post_init__()
        if self.ctx:
            _details = [d for d in self.data.list if d.version == self.data.stable]
            if len(_details) != 1:
                raise Exception(
                    f"Default stable '{self.data.stable}' version not found"
                )
            self.details = _details[0]
