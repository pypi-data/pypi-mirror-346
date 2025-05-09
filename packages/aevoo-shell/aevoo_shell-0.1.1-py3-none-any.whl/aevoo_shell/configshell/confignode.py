from __future__ import annotations

import httpcore
import httpx
import json

# from aiohttp import ClientConnectionError, ClientConnectorError
from configshell import ExecutionError
from configshell_fb import ConfigNode as ConfigNodeDefault
from dataclasses import dataclass, field

# from gql.transport.exceptions import TransportServerError
from pprint import pprint
from typing import TYPE_CHECKING, Coroutine

from aevoo_pycontrol.graphql_client import (
    GraphQLClientGraphQLMultiError,
    GraphQLClientInvalidResponseError,
    BaseModel,
)
from aevoo_shell.utils import async_run

if TYPE_CHECKING:
    from pydantic.main import IncEx
    from aevoo_shell import Root
    from aevoo_pycontrol import Context
    from configshell import ConfigShell


def print_pretty(data, exclude: IncEx = None):
    if isinstance(data, BaseModel):
        data = data.model_dump(exclude=exclude)
    print(json.dumps(data, indent=2))


ConnectionsErrors = (
    # ClientConnectionError,
    # ClientConnectorError,
    ConnectionAbortedError,
    ConnectionResetError,
    ConnectionRefusedError,
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.RemoteProtocolError,
    # TransportServerError,
    httpcore.RemoteProtocolError,
)


@dataclass(eq=False, repr=False)
class ConfigNode(ConfigNodeDefault):
    components_name = None
    help_intro = """
                 GENERALITIES
                 ============
                 The available commands depend on the current path or target
                 path you want to run a command in: different path have
                 different sets of available commands.

                 Please try `help cd` for navigation tips.

                 COMMAND SYNTAX
                 ==============
                 Commands are built using the following syntax:

                 [TARGET_PATH] COMMAND_NAME [OPTIONS]

                 TARGET_PATH indicates the path to run the command from.
                 If omitted, the command is run from your current path.

                 OPTIONS depend on the command. Please use `help` to
                 get more information.
                 """
    ls_reload = False

    children: set[ConfigNode] = field(init=False)
    data: any = None
    name: str
    ctx: Context = None
    loaded: bool = False
    parent: ConfigNode = None
    _shell: ConfigShell = None
    _read_only: bool = True

    @property
    def cid(self):
        if self.data and self.data.cid:
            return self.data.cid

    def execute_command(self, command, pparams=[], kparams={}):
        try:
            return super().execute_command(command, pparams, kparams)
        except (ExecutionError, GraphQLClientGraphQLMultiError) as e:
            self.shell.con.raw_write(f"ERROR : {e}\n")

    def exist(self, name: str):
        return name in {c.name for c in self.children}

    def get_child(self, name):
        child: ConfigNode = super().get_child(name)
        child.load()
        return child

    def get_node(self, path):
        node: ConfigNode = super().get_node(path)
        node.load()
        return node

    def get_root(self) -> Root:
        return super().get_root()

    def level(self, _incr: int = 0):
        if self.is_root():
            return _incr
        return self.parent.level(_incr + 1)

    def load(self, _force: bool = False):
        if not self.loaded or _force:
            shell: ConfigShell = self.shell
            shell.log.debug(f"[{self.path}] Loading")
            self._load()
        self.loaded = True

    def prompt_msg(self):
        _msg = self.name
        _summary, _status = self.summary()
        if _summary != "":
            _msg += f" [{_summary}]"
        if self._read_only:
            _msg += " (RO)"
        return _msg

    # async def summary(self):
    #     return 'OK', True

    def ui_command_data(self):
        pprint(self.data)

    def ui_command_info(self):
        if self.data:
            pprint(self.data)

    def ui_command_ls(self, path=None, depth=None):
        if self.ls_reload:
            self._reload()
        if self.components_name:
            self.shell.con.display(self.components_name)
        super().ui_command_ls(path, depth)

    def ui_command_reload(self):
        self._reload()

    def _eval(self, cor: Coroutine, _reload: bool = False):
        try:
            result = async_run(cor)
            # print(result)
            if _reload:
                self.load(_force=True)
            return result
        except GraphQLClientInvalidResponseError as e:
            self.shell.con.raw_write(f"Error : {e}\n")
        except ConnectionsErrors as e:
            self.shell.con.raw_write(f"Connection error\n")

    def _load(self): ...

    def _reload(self):
        self._children = set()
        self.load(_force=True)

    def __post_init__(self):
        if self.parent and self.parent.exist(self.name):
            if self.data:
                _self_ = self.parent.get_child(self.name)
                _self_.data = self.data
        else:
            if self.ctx is None:
                self.ctx = self.parent.ctx
            super().__init__(name=self.name, parent=self.parent, shell=self._shell)
