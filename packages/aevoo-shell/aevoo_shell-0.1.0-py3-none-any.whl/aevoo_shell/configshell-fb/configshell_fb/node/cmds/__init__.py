"""
This file is part of ConfigShell.
Copyright (c) 2011-2013 by Datera, Inc

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""

from __future__ import annotations

import asyncio
import inspect
from typing import TYPE_CHECKING

from .bookmarks import CmdBookmarks
from .cd import CmdCd
from .get import CmdGet
from .help import CmdHelp
from .ls import CmdLs
from .set import CmdSet
from ..exception import ExecutionError

if TYPE_CHECKING:
    from configshell_fb import ConfigNode


class Cmds:
    ui_command_method_prefix = "ui_command_"

    def execute_command(
        self: ConfigNode,
        command: str,
        pparams: list[str] = None,
        kparams: dict[str, str] = None,
    ):
        """
        Execute a user command on the node. This works by finding out which is
        the support command method, using ConfigNode naming convention:
        The support method's name is 'PREFIX_COMMAND', where PREFIX is defined
        by ConfigNode.ui_command_method_prefix and COMMAND is the commands's
        name as seen by the user.
        @param command: Name of the command.
        @param pparams: The positional parameters to use.
        @param kparams: The keyword=value parameters to use.
        @return: The support method's return value.
        See ConfigShell._execute_command() for expected return values and how
        they are interpreted by ConfigShell.
        @rtype: str or ConfigNode or None
        """
        if pparams is None:
            pparams = []
        if kparams is None:
            kparams = {}

        self.shell.log.debug(
            f"Executing command {command} with pparams {pparams} and kparams {kparams}"
        )

        if command in self.list_commands():
            method = self.get_command_method(command)
        else:
            raise ExecutionError(f"Command not found {command}")

        self.assert_params(method, pparams, kparams)
        result = method(*pparams, **kparams)
        if asyncio.iscoroutine(result):
            result = self.shell.run_async(result)
        return result

    def get_command_description(self: ConfigNode, command: str):
        """
        @return: An description string for a user command.
        @rtype: str
        @param command: The command to describe.
        """
        doc = self.get_command_method(command).__doc__
        if not doc:
            doc = "No description available."
        return self.shell.con.dedent(doc)

    def get_command_method(self: ConfigNode, command: str):
        """
        @param command: The command to get the method for.
        @return: The user command support method.
        @rtype: method
        @raise ValueError: If the command is not found.
        """
        prefix = self.ui_command_method_prefix
        if command in self.list_commands():
            return getattr(self, f"{prefix}{command}")
        else:
            self.shell.log.debug(
                f"No command named {command} in {self.name} ({self.path})"
            )
            raise ValueError(f'No command named "{command}".')

    def get_command_syntax(self: ConfigNode, command: str):
        """
        @return: A list of formatted syntax descriptions for the command:
            - (syntax, comments, default_values)
            - syntax is the syntax definition line.
            - comments is a list of additionnal comments about the syntax.
            - default_values is a string with the default parameters values.
        @rtype: (str, [str...], str)
        @param command: The command to document.
        """
        method = self.get_command_method(command)
        spec = inspect.getfullargspec(method)
        parameters = spec.args[1:]
        if spec.defaults is None:
            num_defaults = 0
        else:
            num_defaults = len(spec.defaults)

        if num_defaults != 0:
            required_parameters = parameters[:-num_defaults]
            optional_parameters = parameters[-num_defaults:]
        else:
            required_parameters = parameters
            optional_parameters = []

        self.shell.log.debug("Required: %s" % str(required_parameters))
        self.shell.log.debug("Optional: %s" % str(optional_parameters))

        syntax = "%s " % command

        required_parameters_str = ""
        for param in required_parameters:
            required_parameters_str += "%s " % param
        syntax += required_parameters_str

        optional_parameters_str = ""
        for param in optional_parameters:
            optional_parameters_str += "[%s] " % param
        syntax += optional_parameters_str

        comments = []
        if spec.varargs is not None:
            syntax += "[%s...] " % spec.varargs
        if spec.varkw is not None:
            syntax += "[%s=value...] " % (spec.varkw)

        default_values = ""
        if num_defaults > 0:
            for index, param in enumerate(optional_parameters):
                if spec.defaults[index] is not None:
                    default_values += "%s=%s " % (param, str(spec.defaults[index]))

        return syntax, comments, default_values

    def get_command_signature(self: ConfigNode, command: str):
        """
        Get a command's signature.
        @param command: The command to get the signature of.
        @return: (parameters, free_pparams, free_kparams) where parameters is a
        list of all the command's parameters and free_pparams and free_kparams
        booleans set to True is the command accepts an arbitrary number of,
        respectively, pparams and kparams.
        @rtype: ([str...], bool, bool)
        """
        method = self.get_command_method(command)
        spec = inspect.getfullargspec(method)
        parameters = spec.args[1:]
        if spec.varargs is not None:
            free_pparams = spec.varargs
        else:
            free_pparams = False
        if spec.varkw is not None:
            free_kparams = spec.varkw
        else:
            free_kparams = False
        self.shell.log.debug(
            "Signature is %s, %s, %s."
            % (str(parameters), str(free_pparams), str(free_kparams))
        )
        return parameters, free_pparams, free_kparams

    def get_completion_method(self, command: str):
        """
        @return: A user command's completion method or None.
        @rtype: method or None
        @param command: The command to get the completion method for.
        """
        prefix = self.ui_complete_method_prefix
        try:
            method = getattr(self, f"{prefix}{command}")
        except AttributeError:
            return None
        else:
            return method

    def list_commands(self):
        """
        @return: The list of user commands available for this node.
        @rtype: list of str
        """
        prefix = self.ui_command_method_prefix
        prefix_len = len(prefix)
        return tuple(
            [
                name[prefix_len:]
                for name in dir(self)
                if name.startswith(prefix)
                and name != prefix
                and inspect.ismethod(getattr(self, name))
            ]
        )

    def ui_command_exit(self: ConfigNode):
        """
        Exits the command line interface.
        """
        return "EXIT"

    def ui_command_pwd(self: ConfigNode):
        """
        Displays the current path.

        SEE ALSO
        ========
        ls cd
        """
        self.shell.con.display(self.path)
