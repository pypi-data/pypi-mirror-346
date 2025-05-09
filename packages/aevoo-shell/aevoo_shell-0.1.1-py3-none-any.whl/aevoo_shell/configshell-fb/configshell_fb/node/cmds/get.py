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


class CmdGet:
    def ui_command_get(self: ConfigNode, group: str = None, *parameter):
        """
        Gets the value of one or more configuration parameters in the given
        group.

        Run with no parameter nor group to list all available groups, or
        with just a group name to list all available parameters within that
        group.

        Example: get global color_mode loglevel_console

        SEE ALSO
        ========
        set
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
                raise ExecutionError("Unknown configuration group: %s" % group)

            section = "%s CONFIG GROUP" % group.upper()
            underline1 = "".ljust(len(section), "=")
            parameters = ""
            params = [
                self.get_group_param(group, p_name)
                for p_name in self.list_group_params(group)
            ]
            for p_def in params:
                group_getter = self.get_group_getter(group)
                value = group_getter(p_def["name"])
                type_method = self.get_type_method(p_def["type"])
                value = type_method(value, reverse=True)
                param = "%s=%s" % (p_def["name"], value)
                if p_def["writable"] is False:
                    param += " [ro]"
                underline2 = "".ljust(len(param), "-")
                parameters += "%s\n%s\n%s\n\n" % (
                    param,
                    underline2,
                    p_def["description"],
                )

            self.shell.con.epy_write(
                """%s\n%s\n%s\n""" % (section, underline1, parameters)
            )

        elif group not in self.list_config_groups():
            raise ExecutionError("Unknown configuration group: %s" % group)

        for param in parameter:
            if param not in self.list_group_params(group):
                raise ExecutionError(
                    "No parameter '%s' in group '%s'." % (param, group)
                )

            self.shell.log.debug("About to get the parameter's value.")
            group_getter = self.get_group_getter(group)
            value = group_getter(param)
            p_def = self.get_group_param(group, param)
            type_method = self.get_type_method(p_def["type"])
            value = type_method(value, reverse=True)
            if p_def["writable"]:
                writable = ""
            else:
                writable = "[ro]"
            self.shell.con.display("%s=%s %s" % (param, value, writable))

    def ui_complete_get(
        self: ConfigNode, parameters: dict[str, str], text: str, current_param: str
    ):
        """
        Parameter auto-completion method for user command get.
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
                group_params = [
                    param
                    for param in self.list_group_params(group)
                    if param.startswith(text)
                    if param not in parameters
                ]
                if group_params:
                    completions.extend(group_params)

        if len(completions) == 1 and not completions[0].endswith("="):
            completions = [completions[0] + " "]

        self.shell.log.debug("Returning completions %s." % str(completions))
        return completions
