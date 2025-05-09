from __future__ import annotations

from dataclasses import dataclass
from getpass import getpass
from typing import TYPE_CHECKING

from aevoo_shell.configshell.confignode import ConfigNode, print_pretty
from aevoo_shell.utils import async_run
from aevoo_shell.utils.instance import secret_write_to

if TYPE_CHECKING:
    from aevoo_pycontrol.graphql_client import (
        SaasTransactionListSaasTransactionList,
    )


def instances_load(parent: ConfigNode):
    instances = ConfigNode(name="instances", parent=parent)
    _instances = async_run(
        instances.ctx.api.saas_transaction_list()
    ).saas_transaction_list
    for _transaction in _instances:
        transaction = Transaction(
            data=_transaction, name=_transaction.name, parent=instances
        )


@dataclass(eq=False, repr=False)
class Transaction(ConfigNode):
    data: SaasTransactionListSaasTransactionList = None

    @property
    def api(self):
        return self.parent.ctx.api

    def ui_command_secret_write_to(self, secret: str, file: str):
        get_ = self._eval(
            self.api.saas_transaction_get(details=True, name=self.data.name)
        )
        details = get_.saas_transaction_get.infos.secrets.get(secret)
        if details is None:
            raise Exception("Not Found")
        pwd = getpass()
        result = self._eval(self.api.saas_secret_get(self.data.name, pwd, secret))
        secret_write_to(details, result.saas_secret_get, file)

    def ui_command_info(self):
        infos = self._eval(
            self.parent.ctx.api.saas_transaction_get(details=True, name=self.data.name)
        )
        print_pretty(infos)
