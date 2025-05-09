from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from aevoo_shell.configshell.confignode import ConfigNode
from aevoo_shell.utils.utils import to_bool, confirm

if TYPE_CHECKING:
    from aevoo_pycontrol.graphql_client import (
        CredentialsListCredentialsList,
        CredentialCreateCredentialCreate,
    )
    from .. import Workspace


@dataclass(eq=False, repr=False)
class Credentials(ConfigNode):
    parent: Workspace = None
    profiles_list: list[str] = None

    def ui_command_add(
        self,
        email: str,
        disabled: bool = None,
        profile: str = None,
        read_only: bool = None,
    ):
        if profile is not None and profile not in self.profiles_list:
            print(f"Invalid profile '{profile}' (profiles : {self.profiles_list})")
            return
        credential = self._eval(
            self.ctx.api.credential_create(
                email=email,
                disabled=to_bool(disabled),
                profile=profile,
                read_only=to_bool(read_only),
            ),
            _reload=True,
        ).credential_create
        print(f"Created : {credential}")
        Credential(name=credential.cid, parent=self, data=credential)

    def ui_command_rm(self, cid: str, force=False):
        _child = self.get_child(cid)
        if confirm("Delete"):
            result = self._eval(
                self.ctx.api.credential_delete(email=cid), _reload=True
            ).credential_delete
            if result is False:
                print(f"Error deletion : {result}")
            else:
                self.remove_child(_child)
                print("Deleted")

    def ui_command_update(
        self,
        cid: str,
        disabled: bool = None,
        profile: str = None,
        read_only: bool = None,
    ):
        _child = self.get_child(cid)
        if profile is not None and profile not in self.profiles_list:
            print(f"Invalid profile '{profile}' (profiles : {self.profiles_list})")
            return

        credential = self._eval(
            self.ctx.api.credential_update(
                disabled=to_bool(disabled),
                email=_child.data.email,
                profile=profile,
                read_only=to_bool(read_only),
            ),
            _reload=True,
        ).credential_update
        print(f"Updated : {credential}")
        _child.data = credential

    def ui_command_t_test(self):
        self._eval(self.ctx.api.saas_transaction_get("TEST"))

    def _load(self):
        self.profiles_list = self._eval(self.ctx.api.profiles_list()).profiles_list
        if not isinstance(self.profiles_list, list):
            print("Context not correctly loaded (RO setting)")
        else:
            self._read_only = False
        for credential in self._eval(self.ctx.api.credentials_list()).credentials_list:
            Credential(name=credential.cid, parent=self, data=credential)


@dataclass(eq=False, repr=False)
class Credential(ConfigNode):
    data: CredentialsListCredentialsList | CredentialCreateCredentialCreate = None

    def summary(self):
        d = self.data
        _profile = d.profile
        if _profile is None:
            _profile = "client"
        if d.read_only:
            _profile += " (RO)"
        else:
            _profile += " (RW)"
        return f"{self.data.email} - {_profile}", not d.disabled

    def ui_command_info(self):
        print(self.data)
