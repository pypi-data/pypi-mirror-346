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


class CmdBookmarks:
    def ui_command_bookmarks(self: ConfigNode, action: str, bookmark: str = None):
        """
        Manage your bookmarks.

        Note that you can also access your bookmarks with the
        `cd` command. For instance, the following commands
        are equivalent:
            - `cd @mybookmark`
            - `bookmarks go mybookmark``

        You can also use bookmarks anywhere where you would use
        a normal path:
            - `@mybookmark ls` performs the `ls` command
            in the bookmarked path.
            - `ls @mybookmark` shows you the objects tree from
            the bookmarked path.


        PARAMETERS
        ==========

        action
        ------
        The "action" parameter is one of:
            - `add` adds the current path to your bookmarks.
            - `del` deletes a bookmark.
            - `go` takes you to a bookmarked path.
            - `show` shows you all your bookmarks.

        bookmark
        --------
        This is the name of the bookmark.

        SEE ALSO
        ========
        ls cd
        """
        if action == "add" and bookmark:
            if bookmark in self.shell.prefs["bookmarks"]:
                raise ExecutionError("Bookmark %s already exists." % bookmark)

            self.shell.prefs["bookmarks"][bookmark] = self.path
            # No way Prefs is going to account for that :-(
            self.shell.prefs.save()
            self.shell.log.info("Bookmarked %s as %s." % (self.path, bookmark))
        elif action == "del" and bookmark:
            if bookmark not in self.shell.prefs["bookmarks"]:
                raise ExecutionError("No such bookmark %s." % bookmark)

            del self.shell.prefs["bookmarks"][bookmark]
            # No way Prefs is going to account for that deletion
            self.shell.prefs.save()
            self.shell.log.info("Deleted bookmark %s." % bookmark)
        elif action == "go" and bookmark:
            if bookmark not in self.shell.prefs["bookmarks"]:
                raise ExecutionError("No such bookmark %s." % bookmark)
            return self.ui_command_cd(self.shell.prefs["bookmarks"][bookmark])
        elif action == "show":
            bookmarks = self.shell.con.dedent(
                """
                                              BOOKMARKS
                                              =========

                                              """
            )
            if not self.shell.prefs["bookmarks"]:
                bookmarks += "No bookmarks yet.\n"
            else:
                for bookmark, path in self.shell.prefs["bookmarks"].items():
                    if len(bookmark) == 1:
                        bookmark += "\0"
                    underline = "".ljust(len(bookmark), "-")
                    bookmarks += "%s\n%s\n%s\n\n" % (bookmark, underline, path)
            self.shell.con.epy_write(bookmarks)
        else:
            raise ExecutionError("Syntax error, see 'help bookmarks'.")

    def ui_complete_bookmarks(
        self: ConfigNode, parameters: dict[str, str], text: str, current_param: str
    ):
        """
        Parameter auto-completion method for user command bookmarks.
        @param parameters: Parameters on the command line.
        @param text: Current text of parameter being typed by the user.
        @param current_param: Name of parameter to complete.
        @return: Possible completions
        @rtype: list of str
        """
        completions = []
        if current_param == "action":
            completions = [
                action
                for action in ["add", "del", "go", "show"]
                if action.startswith(text)
            ]
        elif current_param == "bookmark":
            if "action" in parameters:
                if parameters["action"] not in ["show", "add"]:
                    completions = [
                        mark
                        for mark in self.shell.prefs["bookmarks"]
                        if mark.startswith(text)
                    ]

        if len(completions) == 1:
            return [completions[0] + " "]
        else:
            return completions
