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


class CompletionUtils:
    def _path_complete(self: ConfigNode, text: str):
        (basedir, slash, partial_name) = text.rpartition("/")
        basedir += slash
        target = self.get_node(basedir)
        names = [child.name for child in target.children]
        completions = []
        for name in names:
            num_matches = 0
            if name.startswith(partial_name):
                num_matches += 1
                if num_matches == 1:
                    completions.append("%s%s/" % (basedir, name))
                else:
                    completions.append("%s%s" % (basedir, name))
        if len(completions) == 1:
            if not self.get_node(completions[0], _async_load_=True).children:
                completions[0] = completions[0].rstrip("/") + " "

        # Bookmarks
        bookmarks = [
            "@" + bookmark
            for bookmark in self.shell.prefs["bookmarks"]
            if ("@" + bookmark).startswith(text)
        ]
        self.shell.log.debug("Found bookmarks %s." % str(bookmarks))
        if bookmarks:
            completions.extend(bookmarks)

        self.shell.log.debug("Completions are %s." % str(completions))
        return completions
