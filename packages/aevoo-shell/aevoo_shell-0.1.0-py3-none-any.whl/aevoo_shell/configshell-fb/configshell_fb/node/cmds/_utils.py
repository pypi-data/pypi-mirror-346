from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from configshell_fb import ConfigNode, ConfigShell


def sorting_keys(s):
    s = str(s)
    m = re.search(r"(.*?)(\d+$)", s)
    if m:
        return m.group(1), int(m.group(2))
    else:
        return s, 0


def _render_tree(
    shell: ConfigShell,
    root: ConfigNode,
    margin: list[bool] = None,
    depth: int | str = None,
    do_list: bool = False,
):
    """
    Renders an ascii representation of a tree of ConfigNodes.
    @param root: The root node of the tree
    @param margin: Format of the left margin to use for children.
    True results in a pipe, and False results in no pipe.
    Used for recursion only.
    @param depth: The maximum depth of nodes to display, None means
    infinite.
    @param do_list: Return two lists, one with each line text
    representation, the other with the corresponding paths.
    @return: An ascii tree representation or (lines, paths).
    @rtype: str
    """
    lines = []
    paths = []

    node_length = 2
    node_shift = 2
    level = root.path.rstrip("/").count("/")
    if margin is None:
        margin = [0]
        root_call = True
    else:
        root_call = False

    if do_list:
        color = None
    elif not level % 3:
        color = None
    elif not (level - 1) % 3:
        color = "blue"
    else:
        color = "magenta"

    if do_list:
        styles = None
    elif root_call:
        styles = ["bold", "underline"]
    else:
        styles = ["bold"]

    if do_list:
        name = root.name
    else:
        name = shell.con.render_text(root.name, color, styles=styles)
    name_len = len(root.name)

    summary = root.summary()
    # if inspect.iscoroutine(summary):
    #     summary = summary
    (description, is_healthy) = summary
    if not description:
        if is_healthy is True:
            description = "OK"
        elif is_healthy is False:
            description = "ERROR"
        else:
            description = "..."

    description_len = len(description) + 3

    if do_list:
        summary = "["
    else:
        summary = shell.con.render_text(" [", styles=["bold"])

    if is_healthy is True:
        if do_list:
            summary += description
        else:
            summary += shell.con.render_text(description, "green")
    elif is_healthy is False:
        if do_list:
            summary += description
        else:
            summary += shell.con.render_text(description, "red", styles=["bold"])
    else:
        summary += description

    if do_list:
        summary += "]"
    else:
        summary += shell.con.render_text("]", styles=["bold"])

    # Sort ending numbers numerically, so we get e.g. "lun1, lun2, lun10"
    # instead of "lun1, lun10, lun2".
    children = sorted(root.children, key=sorting_keys)
    line = ""

    for pipe in margin[:-1]:
        if pipe:
            line += "|".ljust(node_shift)
        else:
            line += "".ljust(node_shift)

    if shell.prefs["tree_round_nodes"]:
        node_char = "o"
    else:
        node_char = "+"
    line += node_char.ljust(node_length, "-")
    line += " "
    margin_len = len(line)

    pad = (shell.con.get_width() - 1 - description_len - margin_len - name_len) * "."
    if not do_list:
        pad = shell.con.render_text(pad, color)

    line += name
    if shell.prefs["tree_status_mode"]:
        line += " %s%s" % (pad, summary)

    lines.append(line)
    paths.append(root.path)

    if root_call and not shell.prefs["tree_show_root"] and not do_list:
        tree = ""
        for child in children:
            tree += _render_tree(shell, child, [False], depth)
    else:
        tree = line + "\n"
        if depth is None or depth > 0:
            if depth is not None:
                depth -= 1
            for i in range(len(children)):
                margin.append(i < len(children) - 1)
                if do_list:
                    new_lines, new_paths = _render_tree(
                        shell, children[i], margin, depth, do_list=True
                    )
                    lines.extend(new_lines)
                    paths.extend(new_paths)
                else:
                    tree += _render_tree(shell, children[i], margin, depth)
                margin.pop()

    if root_call:
        if do_list:
            return lines, paths
        else:
            return tree[:-1]
    else:
        if do_list:
            return lines, paths
        else:
            return tree
