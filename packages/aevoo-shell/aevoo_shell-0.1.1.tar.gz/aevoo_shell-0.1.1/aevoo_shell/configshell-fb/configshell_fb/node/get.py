from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aevoo_shell import Root
    from configshell_fb import ConfigNode


class NodeGet:
    def get_child(self: ConfigNode, name: str):
        """
        @param name: The child's name.
        @return: Our child named by name.
        @rtype: ConfigNode
        @raise ValueError: If there is no child named by name.
        """
        for child in self.children:
            if child.name == name:
                return child
        else:
            raise ValueError(f"'No such path {self.path.rstrip('/')}/{name}'")

    def get_node(self: ConfigNode, path: str, _async_load_=False) -> ConfigNode:
        if path is None or path == "":
            path = "."

        # Is it a bookmark ?
        if path.startswith("@"):
            bookmark = path.lstrip("@").strip()
            if bookmark in self.shell.prefs["bookmarks"]:
                path = self.shell.prefs["bookmarks"][bookmark]
            else:
                raise ValueError(f"No such bookmark {bookmark}")

        # Remove duplicate 'separator'
        path = re.sub(f"{self._path_separator}+", self._path_separator, path)
        if len(path) > 1:
            path = path.rstrip(self._path_separator)

        _msg = f"Looking for path '{path}'"
        if _async_load_ is True:
            _msg += " (async node load)"
        self.shell.log.debug(_msg)

        # Absolute path - make relative and pass on to root node
        if path.startswith(self._path_separator):
            next_node = self.get_root()
            next_path = path.lstrip(self._path_separator)
            if next_path:
                return next_node.get_node(next_path, _async_load_=_async_load_)
            else:
                return next_node

        # Relative path
        if self._path_separator in path:
            next_node_name, next_path = path.split(self._path_separator, 1)
            next_node = self.get_node_adjacent(next_node_name)
            if _async_load_ is True:
                self.shell.run_async(next_node.load())
            return next_node.get_node(next_path, _async_load_=_async_load_)

        # Path is just one of our children
        _node = self.get_node_adjacent(path)
        if _async_load_ is True:
            self.shell.run_async(_node.load())
        return _node

    def get_node_adjacent(self: ConfigNode, name: str):
        """
        Returns an adjacent node or ourself.
        """
        if name == self._path_current:
            return self
        elif name == self._path_previous:
            if self.parent is not None:
                return self.parent
            else:
                return self
        else:
            return self.get_child(name)

    def get_root(self: ConfigNode) -> Root:
        """
        @return: The root node of the nodes tree.
        @rtype: ConfigNode
        """
        if self.is_root():
            return self
        else:
            return self.parent.get_root()
