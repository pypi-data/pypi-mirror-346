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

from typing import TYPE_CHECKING, Coroutine

from ._utils import _render_tree
from ..exception import ExecutionError

if TYPE_CHECKING:
    from configshell_fb import ConfigNode


def _lines_walker(lines: list[str], start_pos: int):
    """
    Using the curses urwid library, displays all lines passed as argument,
    and after allowing selection of one line using up, down and enter keys,
    returns its index.
    @param lines: The lines to display and select from.
    @param start_pos: The index of the line to select initially.
    @return: the index of the selected line.
    @rtype: int
    """
    import urwid

    palette = [
        ("header", "white", "black"),
        ("reveal focus", "black", "yellow", "standout"),
    ]

    content = urwid.SimpleListWalker(
        [
            urwid.AttrMap(w, None, "reveal focus")
            for w in [urwid.Text(line) for line in lines]
        ]
    )

    listbox = urwid.ListBox(content)
    frame = urwid.Frame(listbox)

    def handle_input(input, raw):
        for key in input:
            widget, pos = content.get_focus()
            if key == "up":
                if pos > 0:
                    content.set_focus(pos - 1)
            elif key == "down":
                try:
                    content.set_focus(pos + 1)
                except IndexError:
                    pass
            elif key == "enter":
                raise urwid.ExitMainLoop()

    content.set_focus(start_pos)
    loop = urwid.MainLoop(frame, palette, input_filter=handle_input)
    loop.run()
    return listbox.focus_position


class CmdCd:
    def ui_command_cd(self: ConfigNode, path: str = None):
        """
        Change current path to path.

        The path is constructed just like a unix path, with "/" as separator
        character, "." for the current node, ".." for the parent node.

        Suppose the nodes tree looks like this:
           +-/
           +-a0      (1)
           | +-b0    (*)
           |  +-c0
           +-a1      (3)
             +-b0
              +-c0
               +-d0  (2)

        Suppose the current node is the one marked (*) at the beginning of all
        the following examples:
            - `cd ..` takes you to the node marked (1)
            - `cd .` makes you stay in (*)
            - `cd /a1/b0/c0/d0` takes you to the node marked (2)
            - `cd ../../a1` takes you to the node marked (3)
            - `cd /a1` also takes you to the node marked (3)
            - `cd /` takes you to the root node "/"
            - `cd /a0/b0/./c0/../../../a1/.` takes you to the node marked (3)

        You can also navigate the path history with "<" and ">":
            - `cd <` takes you back one step in the path history
            - `cd >` takes you one step forward in the path history

        SEE ALSO
        ========
        ls cd
        """
        self.shell.log.debug(f"Changing current node to '{path}'.")

        if self.shell.prefs["path_history"] is None:
            self.shell.prefs["path_history"] = [self.path]
            self.shell.prefs["path_history_index"] = 0

        # Go back in history to the last existing path
        if path == "<":
            if self.shell.prefs["path_history_index"] == 0:
                self.shell.log.info("Reached begining of path history.")
                return self
            exists = False
            while not exists:
                if self.shell.prefs["path_history_index"] > 0:
                    self.shell.prefs["path_history_index"] = (
                        self.shell.prefs["path_history_index"] - 1
                    )
                    index = self.shell.prefs["path_history_index"]
                    path = self.shell.prefs["path_history"][index]
                    try:
                        target_node = self.get_node(path)
                    except ValueError:
                        pass
                    else:
                        exists = True
                else:
                    path = "/"
                    self.shell.prefs["path_history_index"] = 0
                    self.shell.prefs["path_history"][0] = "/"
                    exists = True
            self.shell.log.info("Taking you back to %s." % path)
            return self.get_node(path)

        # Go forward in history
        if path == ">":
            if (
                self.shell.prefs["path_history_index"]
                == len(self.shell.prefs["path_history"]) - 1
            ):
                self.shell.log.info("Reached the end of path history.")
                return self
            exists = False
            while not exists:
                if (
                    self.shell.prefs["path_history_index"]
                    < len(self.shell.prefs["path_history"]) - 1
                ):
                    self.shell.prefs["path_history_index"] = (
                        self.shell.prefs["path_history_index"] + 1
                    )
                    index = self.shell.prefs["path_history_index"]
                    path = self.shell.prefs["path_history"][index]
                    try:
                        target_node = self.get_node(path)
                    except ValueError:
                        pass
                    else:
                        exists = True
                else:
                    path = self.path
                    self.shell.prefs["path_history_index"] = len(
                        self.shell.prefs["path_history"]
                    )
                    self.shell.prefs["path_history"].append(path)
                    exists = True
            self.shell.log.info("Taking you back to %s." % path)
            return self.get_node(path)

        # Use an urwid walker to select the path
        if path is None:
            lines, paths = _render_tree(self.shell, self.get_root(), do_list=True)
            start_pos = paths.index(self.path)
            selected = _lines_walker(lines, start_pos=start_pos)
            path = paths[selected]

        # Normal path
        try:
            target_node = self.get_node(path, _async_load_=True)
        except ValueError as msg:
            raise ExecutionError(str(msg))

        index = self.shell.prefs["path_history_index"]
        if target_node.path != self.shell.prefs["path_history"][index]:
            # Truncate the hostory to retain current path as last one
            self.shell.prefs["path_history"] = self.shell.prefs["path_history"][
                : index + 1
            ]
            # Append the new path and update the index
            self.shell.prefs["path_history"].append(target_node.path)
            self.shell.prefs["path_history_index"] = index + 1
        self.shell.log.debug(
            "After cd, path history is: %s, index is %d"
            % (
                str(self.shell.prefs["path_history"]),
                self.shell.prefs["path_history_index"],
            )
        )
        return target_node

    def ui_complete_cd(
        self: ConfigNode, parameters: dict[str, str], text: str, current_param: str
    ):
        """
        Parameter auto-completion method for user command cd.
        @param parameters: Parameters on the command line.
        @param text: Current text of parameter being typed by the user.
        @param current_param: Name of parameter to complete.
        @return: Possible completions
        @rtype: list of str
        """

        if current_param == "path":
            completions: list[str] | Coroutine[any, any, list[str]]
            completions = self.ui_complete_ls(parameters, text, current_param)
            completions.extend([nav for nav in ["<", ">"] if nav.startswith(text)])
            return completions
