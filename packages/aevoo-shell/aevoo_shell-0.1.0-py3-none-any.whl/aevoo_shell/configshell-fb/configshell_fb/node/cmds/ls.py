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

from ._utils import _render_tree
from ..exception import ExecutionError

if TYPE_CHECKING:
    from configshell_fb import ConfigNode


class CmdLs:
    def ui_command_ls(self: ConfigNode, path: str = None, depth: int | str = None):
        """
        Display either the nodes tree relative to path or to the current node.

        PARAMETERS
        ==========

        path
        ----
        The path to display the nodes tree of. Can be an absolute path, a
        relative path or a bookmark.

        depth
        -----
        The depth parameter limits the maximum depth of the tree to display.
        If set to 0, then the complete tree will be displayed (the default).

        SEE ALSO
        ========
        cd bookmarks
        """
        try:
            target = self.get_node(path, _async_load_=True)
        except ValueError as msg:
            raise ExecutionError(str(msg))

        if depth is None:
            depth = self.shell.prefs["tree_max_depth"]
        try:
            depth = int(depth)
        except ValueError:
            raise ExecutionError("The tree depth must be a number.")

        if depth == 0:
            depth = None
        tree = _render_tree(self.shell, target, depth=depth)
        self.shell.con.display(tree)

    def ui_complete_ls(
        self: ConfigNode, parameters: dict[str, str], text: str, current_param: str
    ):
        """
        Parameter auto-completion method for user command ls.
        @param parameters: Parameters on the command line.
        @param text: Current text of parameter being typed by the user.
        @param current_param: Name of parameter to complete.
        @return: Possible completions
        @rtype: list of str
        """
        if current_param == "path":
            return self._path_complete(text)

        elif current_param == "depth":
            if text:
                try:
                    int(text.strip())
                except ValueError:
                    self.shell.log.debug("Text is not a number.")
                    return []
            return [
                text + number
                for number in [str(num) for num in range(10)]
                if (text + number).startswith(text)
            ]
