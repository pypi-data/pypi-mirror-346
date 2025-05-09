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

import inspect
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Awaitable

from .cmds import (
    CmdBookmarks,
    CmdCd,
    CmdGet,
    CmdHelp,
    CmdLs,
    CmdSet,
    Cmds,
)
from .completion_utils import CompletionUtils
from .exception import ExecutionError
from .get import NodeGet
from .param_type import ParamTypes

if TYPE_CHECKING:
    from configshell_fb import ConfigShell


@dataclass(eq=False, repr=False)
class ConfigNode(
    CmdBookmarks,
    CmdCd,
    CmdGet,
    CmdHelp,
    CmdLs,
    CmdSet,
    Cmds,
    CompletionUtils,
    NodeGet,
    ParamTypes,
):
    """
    The ConfigNode class defines a common skeleton to be used by specific
    implementation. It is "purely virtual" (sorry for using non-pythonic
    vocabulary there ;-) ).
    """

    _path_separator = "/"
    _path_current = "."
    _path_previous = ".."

    ui_type_method_prefix = "ui_type_"
    ui_complete_method_prefix = "ui_complete_"
    ui_setgroup_method_prefix = "ui_setgroup_"
    ui_getgroup_method_prefix = "ui_getgroup_"

    help_intro = """
                 GENERALITIES
                 ============
                 This is a shell in which you can create, delete and configure
                 configuration objects.

                 The available commands depend on the current path or target
                 path you want to run a command in: different path have
                 different sets of available commands, i.e. a path pointing at
                 an iSCSI target will not have the same available commands as,
                 say, a path pointing at a storage object.

                 The prompt that starts each command line indicates your
                 current path. Alternatively (useful if the prompt displays
                 an abbreviated path to save space), you can run the
                 `pwd` command to display the complete current path.

                 Navigating the tree is done using the `cd` command. Without
                 any argument, `cd` presents you with the full objects
                 tree. Just use arrows to select the destination path, and
                 enter will get you there. Please try `help cd` for navigation
                 tips.

                 COMMAND SYNTAX
                 ==============
                 Commands are built using the following syntax:

                 [TARGET_PATH] COMMAND_NAME [OPTIONS]

                 TARGET_PATH indicates the path to run the command from.
                 If omitted, the command is run from your current path.

                 OPTIONS depend on the command. Please use `help` to
                 get more information.
                 """

    name: str

    children: set[ConfigNode] = field(init=False)
    loaded: bool = field(default=False)
    parent: ConfigNode = None
    _shell: ConfigShell = None

    @property
    def path(self):
        """
        @returns: The absolute path for this node.
        @rtype: str
        """
        subpath = self._path_separator + self.name
        if self.is_root():
            return self._path_separator
        elif self.parent.is_root():
            return subpath
        else:
            return self.parent.path + subpath

    @property
    def shell(self):
        """
        Gets the shell attached to ConfigNode tree.
        """
        if self.is_root():
            return self._shell
        else:
            return self.get_root().shell

    def assert_params(self, method, pparams: list[str], kparams: dict[str, str]):
        """
        Checks that positional and keyword parameters match a method
        definition, or raise an ExecutionError.
        @param method: The method to check call signature against.
        @param pparams: The positional parameters.
        @param kparams: The keyword parameters.
        @raise ExecutionError: When the check fails.
        """
        spec = inspect.getfullargspec(method)
        args = spec.args[1:]
        pp = spec.varargs
        kw = spec.varkw

        if spec.defaults is None:
            nb_opt_params = 0
        else:
            nb_opt_params = len(spec.defaults)
        nb_max_params = len(args)
        nb_min_params = nb_max_params - nb_opt_params

        req_params = args[:nb_min_params]
        opt_params = args[nb_min_params:]

        unexpected_keywords = sorted(set(kparams) - set(args))
        missing_params = sorted(
            set(args[len(pparams) :]) - set(opt_params) - set(kparams.keys())
        )

        nb_params = len(pparams) + len(kparams)
        nb_standard_params = len(pparams) + len(
            [param for param in kparams if param in args]
        )
        nb_extended_params = nb_params - nb_standard_params

        self.shell.log.debug("Min params: %d" % nb_min_params)
        self.shell.log.debug("Max params: %d" % nb_max_params)
        self.shell.log.debug("Required params: %s" % ", ".join(req_params))
        self.shell.log.debug("Optional params: %s" % ", ".join(opt_params))
        self.shell.log.debug("Got %s standard params." % nb_standard_params)
        self.shell.log.debug("Got %s extended params." % nb_extended_params)
        self.shell.log.debug("Variable positional params: %s" % pp)
        self.shell.log.debug("Variable keyword params: %s" % kw)

        if len(missing_params) == 1:
            raise ExecutionError(f"Missing required parameter '{missing_params[0]}'")
        elif missing_params:
            raise ExecutionError(
                "Missing required parameters %s"
                % ", ".join("'%s'" % missing for missing in missing_params)
            )

        if kw is None:
            if len(unexpected_keywords) == 1:
                raise ExecutionError(
                    f"Unexpected keyword parameter '{unexpected_keywords[0]}'."
                )
            elif unexpected_keywords:
                raise ExecutionError(
                    "Unexpected keyword parameters %s."
                    % ", ".join("'%s'" % kw for kw in unexpected_keywords)
                )
        all_params = args[: len(pparams)]
        all_params.extend(kparams.keys())
        for param in all_params:
            if all_params.count(param) > 1:
                raise ExecutionError(f"Duplicate parameter '{param}'.")

        if nb_opt_params == 0 and nb_standard_params != nb_min_params and pp is None:
            raise ExecutionError(
                f"Got {nb_standard_params} positionnal parameters, expected exactly {nb_min_params}."
            )

        if nb_standard_params > nb_max_params and pp is None:
            raise ExecutionError(
                f"Got {nb_standard_params} positionnal parameters, expected at most {nb_max_params}."
            )

    def get_group_getter(self, group: str):
        """
        @param group: A valid configuration group
        @return: The getter method for the configuration group.
        @rtype: method object
        """
        prefix = self.ui_getgroup_method_prefix
        return getattr(self, "%s%s" % (prefix, group))

    def get_group_param(self, group: str, param: str):
        """
        @param group: The configuration group to retreive the parameter from.
        @param param: The parameter name.
        @return: A dictionnary for the requested group parameter, with
        name, writable, description, group and type fields.
        @rtype: dict
        @raise ValueError: If the parameter or group does not exist.
        """
        if group not in self.list_config_groups():
            raise ValueError(f"Not such configuration group {group}")
        if param not in self.list_group_params(group):
            raise ValueError(
                f"Not such parameter {param} in configuration group {group}"
            )
        (p_type, p_description, p_writable) = self._configuration_groups[group][param]

        return dict(
            name=param,
            group=group,
            type=p_type,
            description=p_description,
            writable=p_writable,
        )

    def get_group_setter(self, group: str):
        """
        @param group: A valid configuration group
        @return: The setter method for the configuration group.
        @rtype: method object
        """
        prefix = self.ui_setgroup_method_prefix
        return getattr(self, "%s%s" % (prefix, group))

    def get_type_method(self, type_: str):
        """
        Returns the type helper method matching the type name.
        """
        return getattr(self, f"{self.ui_type_method_prefix}{type_}")

    def define_config_group_param(
        self,
        group: str,
        param: str,
        type_: str,
        description: str = None,
        writable: bool = True,
    ):
        """
        Helper to define configuration group parameters.
        @param group: The configuration group to add the parameter to.
        @param param: The new parameter name.
        @param description: Optional description string.
        @param writable: Whether or not this would be a rw or ro parameter.
        """
        if group not in self._configuration_groups:
            self._configuration_groups[group] = {}

        if description is None:
            description = f"The {param} {group} parameter."

        # Fail early if the type and set/get helpers don't exist
        self.get_type_method(type_)
        self.get_group_getter(group)
        if writable:
            self.get_group_setter(group)

        self._configuration_groups[group][param] = [type_, description, writable]

    def exist(self, name: str):
        return name in [c.name for c in self.children]

    def is_root(self):
        """
        @return: Wether or not we are a root node.
        @rtype: bool
        """
        if self.parent is None:
            return True
        else:
            return False

    def list_config_groups(self):
        """
        Lists the configuration group names.
        """
        return self._configuration_groups.keys()

    def list_group_params(self, group: str, writable: bool = None):
        """
        Lists the parameters from group matching the optional param, writable
        and type supplied (if none is supplied, returns all group parameters.
        @param group: The group to list parameters of.
        @param writable: Optional writable flag filter.
        """
        if group not in self.list_config_groups():
            return []
        else:
            params = []
            for p_name, p_def in self._configuration_groups[group].items():
                (p_type, p_description, p_writable) = p_def
                if writable is not None and p_writable != writable:
                    continue
                params.append(p_name)

            params.sort()
            return params

    async def load(self):
        if self.loaded is False:
            self.shell.log.debug(f"[{self.path}] Loading")
            await self._load()
        self.loaded = True

    def prompt_msg(self):
        return ""

    def remove_child(self, child: ConfigNode | str):
        """
        Removes a child from our children's list.
        @param child: The child to remove.
        """
        if isinstance(child, str):
            child = self.get_child(child)
        self.children.remove(child)

    def summary(self):
        """
        Returns a tuple with a status/description string for this node and a
        health flag, to be displayed along the node's name in object trees,
        etc.
        @returns: (description, is_healthy)
        @rtype: (str, bool or None)
        """
        return "", None

    def ui_command_reload(self) -> Awaitable:
        self.loaded = False
        self.children = set()
        return self.ui_command_cd(".")

    def ui_setgroup_global(self, parameter: str, value):
        """
        This is the backend method for setting parameters in configuration
        group 'global'. It simply uses the Prefs() backend to store the global
        preferences for the shell. Some of these group parameters are shared
        using the same Prefs() object by the Log() and Console() classes, so
        this backend should not be changed without taking this into
        consideration.

        The parameters getting to us have already been type-checked and casted
        by the type-check methods registered in the config group via the ui set
        command, and their existence in the group has also been checked. Thus
        our job is minimal here. Also, it means that overhead when called with
        generated arguments (as opposed to user-supplied) gets minimal
        overhead, and allows setting new parameters without error.

        @param parameter: The parameter to set.
        @param value: The value
        """
        self.shell.prefs[parameter] = value

    def ui_getgroup_global(self, parameter: str):
        """
        This is the backend method for getting configuration parameters out of
        the global configuration group. It gets the values from the Prefs()
        backend. Eventual casting to str for UI display is handled by the ui
        get command, for symmetry with the pendant ui_setgroup method.
        Existence of the parameter in the group should have already been
        checked by the ui get command, so we go blindly about this. This might
        allow internal client code to get a None value if the parameter does
        not exist, as supported by Prefs().

        @param parameter: The parameter to get the value of.
        @return: The parameter's value
        @rtype: arbitrary
        """
        return self.shell.prefs[parameter]

    def ui_eval_param(self, ui_value: str, type_: str, default):
        """
        Evaluates a user-provided parameter value using a given type helper.
        If the parameter value is None, the default will be returned. If the
        ui_value does not check out with the type helper, and execution error
        will be raised.

        @param ui_value: The user provided parameter value.
        @param type_: The ui_type to be used
        @param default: The default value to return.
        @return: The evaluated parameter value.
        @rtype: depends on type
        @raise ExecutionError: If evaluation fails.
        """
        type_method = self.get_type_method(type_)
        if ui_value is None:
            return default
        else:
            try:
                value = type_method(ui_value)
            except ValueError as msg:
                raise ExecutionError(msg)
            else:
                return value

    async def _load(self):
        pass

    def __post_init__(self):
        if self.parent is None:
            if self._shell is None:
                raise ValueError("A root ConfigNode must have a shell.")
            else:
                self._shell.attach_root_node(self)
        else:
            if self._shell is not None:
                raise ValueError("A non-root ConfigNode can't have a shell.")

            if self.parent.exist(self.name):
                # raise ValueError(f"Name {self.name} already used by a sibling.")
                self.parent.remove_child(self.name)
            self.parent.children.add(self)

        self._configuration_groups: dict[str, dict[str, list[str, str, str]]] = {}

        self.define_config_group_param(
            "global", "tree_round_nodes", "bool", "Tree node display style."
        )
        self.define_config_group_param(
            "global",
            "tree_status_mode",
            "bool",
            "Whether or not to display status in tree.",
        )
        self.define_config_group_param(
            "global",
            "tree_max_depth",
            "number",
            "Maximum depth of displayed node tree.",
        )
        self.define_config_group_param(
            "global", "tree_show_root", "bool", "Whether or not to display tree root."
        )
        self.define_config_group_param(
            "global", "color_mode", "bool", "Console color display mode."
        )
        self.define_config_group_param(
            "global",
            "loglevel_console",
            "loglevel",
            "Log level for messages going to the console.",
        )
        self.define_config_group_param(
            "global",
            "loglevel_file",
            "loglevel",
            "Log level for messages going to the log file.",
        )
        self.define_config_group_param("global", "logfile", "string", "Logfile to use.")
        self.define_config_group_param(
            "global", "color_default", "colordefault", "Default text display color."
        )
        self.define_config_group_param(
            "global", "color_path", "color", "Color to use for path completions"
        )
        self.define_config_group_param(
            "global", "color_command", "color", "Color to use for command completions."
        )
        self.define_config_group_param(
            "global",
            "color_parameter",
            "color",
            "Color to use for parameter completions.",
        )
        self.define_config_group_param(
            "global", "color_keyword", "color", "Color to use for keyword completions."
        )
        self.define_config_group_param(
            "global",
            "prompt_length",
            "number",
            "Max length of the shell prompt path, 0 for infinite.",
        )

        if self.shell.prefs["bookmarks"] is None:
            self.shell.prefs["bookmarks"] = {}

    def __str__(self):
        if self.is_root():
            return "/"
        else:
            return self.name
