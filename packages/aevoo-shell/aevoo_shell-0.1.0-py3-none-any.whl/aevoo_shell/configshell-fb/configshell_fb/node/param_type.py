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

if TYPE_CHECKING:
    from configshell_fb import ConfigNode


class ParamTypes:
    def ui_type_number(
        self: ConfigNode, value=None, enum: bool = False, reverse: bool = False
    ):
        """
        UI parameter type helper for number parameter type.
        @param value: Value to check against the type.
        @param enum: Has a meaning only if value is omitted. If set, returns
        a list of the possible values for the type, or [] if this is not
        possible. If not set, returns a text description of the type format.
        @param reverse: If set, translates an internal value to its UI
        string representation.
        @return: c.f. parameter enum description.
        @rtype: str|list|None
        @raise ValueError: If the value does not check ok against the type.
        """
        if reverse:
            if value is not None:
                return str(value)
            else:
                return "n/a"

        type_enum = []
        syntax = "NUMBER"
        if value is None:
            if enum:
                return type_enum
            else:
                return syntax
        elif not value:
            return None
        else:
            try:
                value = int(value)
            except ValueError:
                raise ValueError(f"Syntax error, {value} is not a {syntax}.")
            else:
                return value

    def ui_type_string(
        self: ConfigNode, value=None, enum: bool = False, reverse: bool = False
    ):
        """
        UI parameter type helper for string parameter type.
        @param value: Value to check against the type.
        @param enum: Has a meaning only if value is omitted. If set, returns
        a list of the possible values for the type, or [] if this is not
        possible. If not set, returns a text description of the type format.
        @param reverse: If set, translates an internal value to its UI
        string representation.
        @return: c.f. parameter enum description.
        @rtype: str|list|None
        @raise ValueError: If the value does not check ok against the type.
        """
        if reverse:
            if value is not None:
                return value
            else:
                return "n/a"

        type_enum = []
        syntax = "STRING_OF_TEXT"
        if value is None:
            if enum:
                return type_enum
            else:
                return syntax
        elif not value:
            return None
        else:
            try:
                value = str(value)
            except ValueError:
                raise ValueError(f"Syntax error, {value} is not a {syntax}.")
            else:
                return value

    def ui_type_bool(
        self: ConfigNode, value=None, enum: bool = False, reverse: bool = False
    ):
        """
        UI parameter type helper for boolean parameter type. Valid values are
        either 'true' or 'false'.
        @param value: Value to check against the type.
        @param enum: Has a meaning only if value is omitted. If set, returns
        a list of the possible values for the type, or None if this is not
        possible. If not set, returns a text description of the type format.
        @param reverse: If set, translates an internal value to its UI
        string representation.
        @return: c.f. parameter enum description.
        @rtype: str|list|None
        @raise ValueError: If the value does not check ok againts the type.
        """
        if reverse:
            if value:
                return "true"
            else:
                return "false"
        type_enum = ["true", "false"]
        syntax = "|".join(type_enum)
        if value is None:
            if enum:
                return type_enum
            else:
                return syntax
        elif value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        else:
            raise ValueError(f"Syntax error, {value} is not a {syntax}.")

    def ui_type_loglevel(
        self: ConfigNode, value=None, enum: bool = False, reverse: bool = False
    ):
        """
        UI parameter type helper for log level parameter type.
        @param value: Value to check against the type.
        @param enum: Has a meaning only if value is omitted. If set, returns
        a list of the possible values for the type, or None if this is not
        possible. If not set, returns a text description of the type format.
        @param reverse: If set, translates an internal value to its UI
        string representation.
        @return: c.f. parameter enum description.
        @rtype: str|list|None
        @raise ValueError: If the value does not check ok againts the type.
        """
        if reverse:
            if value is not None:
                return value
            else:
                return "n/a"

        type_enum = self.shell.log.levels
        syntax = "|".join(type_enum)
        if value is None:
            if enum:
                return type_enum
            else:
                return syntax
        elif value in type_enum:
            return value
        else:
            raise ValueError(f"Syntax error, {value} is not a {syntax}.")

    def ui_type_color(
        self: ConfigNode, value=None, enum: bool = False, reverse: bool = False
    ):
        """
        UI parameter type helper for color parameter type.
        @param value: Value to check against the type.
        @param enum: Has a meaning only if value is omitted. If set, returns
        a list of the possible values for the type, or None if this is not
        possible. If not set, returns a text description of the type format.
        @param reverse: If set, translates an internal value to its UI
        string representation.
        @return: c.f. parameter enum description.
        @rtype: str|list|None
        @raise ValueError: If the value does not check ok againts the type.
        """
        if reverse:
            if value is not None:
                return value
            else:
                return "default"

        type_enum = self.shell.con.colors + ["default"]
        syntax = "|".join(type_enum)
        if value is None:
            if enum:
                return type_enum
            else:
                return syntax
        elif not value or value == "default":
            return None
        elif value in type_enum:
            return value
        else:
            raise ValueError(f"Syntax error, {value} is not a {syntax}.")

    def ui_type_colordefault(
        self: ConfigNode, value=None, enum: bool = False, reverse: bool = False
    ):
        """
        UI parameter type helper for default color parameter type.
        @param value: Value to check against the type.
        @param enum: Has a meaning only if value is omitted. If set, returns
        a list of the possible values for the type, or None if this is not
        possible. If not set, returns a text description of the type format.
        @param reverse: If set, translates an internal value to its UI
        string representation.
        @return: c.f. parameter enum description.
        @rtype: str|list|None
        @raise ValueError: If the value does not check ok againts the type.
        """
        if reverse:
            if value is not None:
                return value
            else:
                return "none"

        type_enum = self.shell.con.colors + ["none"]
        syntax = "|".join(type_enum)
        if value is None:
            if enum:
                return type_enum
            else:
                return syntax
        elif not value or value == "none":
            return None
        elif value in type_enum:
            return value
        else:
            raise ValueError(f"Syntax error, {value} is not a {syntax}.")
