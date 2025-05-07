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

from typing import TYPE_CHECKING

from ..exception import ExecutionError

if TYPE_CHECKING:
    from configshell_fb import ConfigNode


class CmdSet:
    def ui_command_set(self: ConfigNode, group: str = None, **parameter):
        """
        Sets one or more configuration parameters in the given group.
        The "global" group contains all global CLI preferences.
        Other groups are specific to the current path.

        Run with no parameter nor group to list all available groups, or
        with just a group name to list all available parameters within that
        group.

        Example: set global color_mode=true loglevel_console=info

        SEE ALSO
        ========
        get
        """
        if group is None:
            self.shell.con.epy_write(
                """
                                     AVAILABLE CONFIGURATION GROUPS
                                     ==============================
                                     %s
                                     """
                % " ".join(self.list_config_groups())
            )
        elif not parameter:
            if group not in self.list_config_groups():
                raise ExecutionError(f"Unknown configuration group: {group}")

            section = f"{group.upper()} CONFIG GROUP"
            underline1 = "".ljust(len(section), "=")
            parameters = ""
            for p_name in self.list_group_params(group, writable=True):
                p_def = self.get_group_param(group, p_name)
                type_method = self.get_type_method(p_def["type"])
                p_name = "%s=%s" % (p_def["name"], p_def["type"])
                underline2 = "".ljust(len(p_name), "-")
                parameters += "%s\n%s\n%s\n\n" % (
                    p_name,
                    underline2,
                    p_def["description"],
                )
            self.shell.con.epy_write(
                """%s\n%s\n%s\n""" % (section, underline1, parameters)
            )

        elif group not in self.list_config_groups():
            raise ExecutionError("Unknown configuration group: %s" % group)

        for param, value in parameter.items():
            if param not in self.list_group_params(group):
                raise ExecutionError(
                    "Unknown parameter %s in group '%s'." % (param, group)
                )

            p_def = self.get_group_param(group, param)
            type_method = self.get_type_method(p_def["type"])
            if not p_def["writable"]:
                raise ExecutionError("Parameter %s is read-only." % param)

            try:
                value = type_method(value)
            except ValueError as msg:
                raise ExecutionError("Not setting %s! %s" % (param, msg))

            group_setter = self.get_group_setter(group)
            group_setter(param, value)
            group_getter = self.get_group_getter(group)
            value = group_getter(param)
            value = type_method(value, reverse=True)
            self.shell.con.display("Parameter %s is now '%s'." % (param, value))

    def ui_complete_set(
        self: ConfigNode, parameters: dict[str, str], text: str, current_param: str
    ):
        """
        Parameter auto-completion method for user command set.
        @param parameters: Parameters on the command line.
        @param text: Current text of parameter being typed by the user.
        @param current_param: Name of parameter to complete.
        @return: Possible completions
        @rtype: list of str
        """
        completions = []

        self.shell.log.debug(
            "Called with params=%s, text='%s', current='%s'"
            % (str(parameters), text, current_param)
        )

        if current_param == "group":
            completions = [
                group for group in self.list_config_groups() if group.startswith(text)
            ]
        elif "group" in parameters:
            group = parameters["group"]
            if group in self.list_config_groups():
                group_params = self.list_group_params(group, writable=True)
                if current_param in group_params:
                    p_def = self.get_group_param(group, current_param)
                    type_method = self.get_type_method(p_def["type"])
                    type_enum = type_method(enum=True)
                    if type_enum is not None:
                        type_enum = [
                            item for item in type_enum if item.startswith(text)
                        ]
                        completions.extend(type_enum)
                else:
                    group_params = [
                        param + "="
                        for param in group_params
                        if param.startswith(text)
                        if param not in parameters
                    ]
                    if group_params:
                        completions.extend(group_params)

        if len(completions) == 1 and not completions[0].endswith("="):
            completions = [completions[0] + " "]

        self.shell.log.debug("Returning completions %s." % str(completions))
        return completions
