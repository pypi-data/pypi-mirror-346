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

import sys
from asyncio import AbstractEventLoop

import asyncio
import os
# A fix for frozen packages
import signal
from typing import TYPE_CHECKING, Sequence, Coroutine

if TYPE_CHECKING:
    from typing import TextIO

from pyparsing import (
    alphanums,
    locatedExpr,
    OneOrMore,
    Optional,
    ParseResults,
    Regex,
    Suppress,
    Word,
    quotedString,
    removeQuotes,
)

from . import console
from . import log
from . import prefs
from .node import ConfigNode, ExecutionError


def handle_sigint(signum, frame):
    """
    Raise KeyboardInterrupt when we get a SIGINT.
    This is normally done by python, but even after patching
    pyinstaller 1.4 to ignore SIGINT in the C wrapper code, we
    still have to do the translation ourselves.
    """
    raise KeyboardInterrupt


try:
    signal.signal(signal.SIGINT, handle_sigint)
except Exception:
    # In a thread, this fails
    pass

if sys.stdout.isatty():
    import readline

    tty = True
else:
    tty = False

    # remember the original setting
    oldTerm = os.environ.get("TERM")
    os.environ["TERM"] = ""

    import readline

    # restore the orignal TERM setting
    if oldTerm is not None:
        os.environ["TERM"] = oldTerm
    del oldTerm


class ConfigShell(object):
    """
    This is a simple CLI command interpreter that can be used both in
    interactive or non-interactive modes.
    It is based on a tree of ConfigNode objects, which can be navigated.

    The ConfigShell object itself provides global navigation commands.
    It also handles the parsing of local commands (specific to a certain
    ConfigNode) according to the ConfigNode commands definitions.
    If the ConfigNode provides hooks for possible parameter values in a given
    context, then the ConfigShell will also provide command-line completion
    using the TAB key. If no completion hooks are available from the
    ConfigNode, the completion function will still be able to display some help
    and general syntax advice (as much as the ConfigNode will provide).

    Interactive sessions can be saved/loaded automatically by ConfigShell is a
    writable session directory is supplied. This includes command-line history,
    current node and global parameters.
    """

    default_prefs = {
        "color_path": "magenta",
        "color_command": "cyan",
        "color_parameter": "magenta",
        "color_keyword": "cyan",
        "logfile": None,
        "loglevel_console": "info",
        "loglevel_file": "debug9",
        "color_mode": True,
        "prompt_length": 120,
        "tree_max_depth": 0,
        "tree_status_mode": True,
        "tree_round_nodes": True,
        "tree_show_root": False,
    }
    loop: AbstractEventLoop

    _completion_help_topic = ""
    _current_parameter = ""
    _current_token = ""
    _current_completions = []

    def __init__(self, preferences_dir: str = None, loop: AbstractEventLoop = None):
        """
        Creates a new ConfigShell.
        @param preferences_dir: Directory to load/save preferences from/to
        """
        self.loop = loop
        self._current_node: ConfigNode | None = None
        self._root_node: ConfigNode | None = None
        self._exit = False

        # Grammar of the command line
        command = locatedExpr(Word(alphanums + '_'))('command')
        var = Word(alphanums + r'?;&*$!#,=_\+/.<>()~@:-%[]')
        value = quotedString.setParseAction(removeQuotes) | var
        keyword = Word(alphanums + r'_\-')
        kparam = locatedExpr(keyword + Suppress('=') + Optional(value, default=''))('kparams*')
        pparam = locatedExpr(var)('pparams*')
        parameter = kparam | pparam
        parameters = OneOrMore(parameter)
        bookmark = Regex('@([A-Za-z0-9:_.]|-)+')
        pathstd = (
            Regex(r'([A-Za-z0-9:_.\[\]@]|-)*' + '/' + r'([A-Za-z0-9:_.\[\]@/]|-)*')
            | '..'
            | '.'
        )
        path = locatedExpr(bookmark | pathstd | '*')('path')
        parser = Optional(path) + Optional(command) + Optional(parameters)
        self._parser = parser

        if tty:
            readline.set_completer_delims("\t\n ~!#$^&(){}|;'\",?")
            readline.set_completion_display_matches_hook(self._display_completions)

        self.log = log.Log()

        if preferences_dir is not None:
            preferences_dir = os.path.expanduser(preferences_dir)
            if not os.path.exists(preferences_dir):
                os.makedirs(preferences_dir)
            self._prefs_file = preferences_dir + "/prefs.bin"
            self.prefs = prefs.Prefs(self._prefs_file)
            self._cmd_history = preferences_dir + "/history.txt"
            self._save_history = True
            if not os.path.isfile(self._cmd_history):
                try:
                    open(self._cmd_history, "w").close()
                except:
                    self.log.warning(
                        f"Cannot create history file {self._cmd_history}, command history will not be saved."
                    )
                    self._save_history = False

            if os.path.isfile(self._cmd_history) and tty:
                try:
                    readline.read_history_file(self._cmd_history)
                except IOError:
                    self.log.warning(
                        f"Cannot read command history file {self._cmd_history}."
                    )

            if self.prefs["logfile"] is None:
                self.prefs["logfile"] = preferences_dir + "/" + "log.txt"

            self.prefs.autosave = True

        else:
            self.prefs = prefs.Prefs()
            self._save_history = False

        try:
            self.prefs.load()
        except IOError:
            self.log.warning(f"Could not load preferences file {self._prefs_file}.")

        for pref, value in self.default_prefs.items():
            if pref not in self.prefs:
                self.prefs[pref] = value

        self.con = console.Console()

    # Private methods

    def _display_completions(
        self, substitution: str, matches: Sequence[str], max_length: int
    ):
        """
        Display the completions. Invoked by readline.
        @param substitution: string to complete
        @param matches: list of possible matches
        @param max_length: length of the longest matching item
        """

        x_orig = self.con.get_cursor_xy()[0]
        width = self.con.get_width()
        max_length += 2

        def just(text):
            """
            Justifies the text to the max match length.
            """
            return text.ljust(max_length, " ")

        # Sort and colorize the matches
        if self._current_parameter:
            keywords = []
            values = []
            for match in matches:
                if match.endswith("="):
                    keywords.append(
                        self.con.render_text(just(match), self.prefs["color_keyword"])
                    )
                elif "=" in match:
                    _, _, value = match.partition("=")
                    values.append(
                        self.con.render_text(just(value), self.prefs["color_parameter"])
                    )
                else:
                    values.append(
                        self.con.render_text(just(match), self.prefs["color_parameter"])
                    )
            matches = values + keywords
        else:
            paths = []
            commands = []
            for match in matches:
                if "/" in match or match.startswith("@") or "*" in match:
                    paths.append(
                        self.con.render_text(just(match), self.prefs["color_path"])
                    )
                else:
                    commands.append(
                        self.con.render_text(just(match), self.prefs["color_command"])
                    )
            matches = paths + commands

        # Display the possible completions in columns
        self.con.raw_write("\n")
        if matches:
            if max_length < width:
                nr_cols = width // max_length
            else:
                nr_cols = 1

            for i in range(0, len(matches), nr_cols):
                self.con.raw_write("".join(matches[i : i + nr_cols]))
                self.con.raw_write("\n")

        # Display the prompt and the command line
        line = f"{self._get_prompt()}{readline.get_line_buffer()}"
        self.con.raw_write(line)

        # Move the cursor where it should be
        y_pos = self.con.get_cursor_xy()[1]
        self.con.set_cursor_xy(x_orig, y_pos)

    def _complete_token_command(self, text: str, path: str, command: str):
        """
        Completes a partial command token, which could also be the beginning
        of a path.
        @param path: Path of the target ConfigNode.
        @param command: The command (if any) found by the parser.
        @param text: Current text being typed by the user.
        @return: Possible completions for the token.
        @rtype: list of str
        """
        completions = []
        target = self._current_node.get_node(path)
        commands = target.list_commands()
        self.log.debug(f"Completing command token among {str(commands)}")

        # Start with the possible commands
        for command in commands:
            if command.startswith(text):
                completions.append(command)
        if len(completions) == 1:
            completions[0] = completions[0] + " "

        # No identified path yet on the command line, this might be it
        if not path:
            path_completions = [
                child.name + "/"
                for child in self._current_node.children
                if child.name.startswith(text)
            ]
            if not text:
                path_completions.append("/")
                if len(self._current_node.children) > 1:
                    path_completions.append("* ")

            if path_completions:
                if completions:
                    self._current_token = (
                        self.con.render_text("path", self.prefs["color_path"])
                        + "|"
                        + self.con.render_text("command", self.prefs["color_command"])
                    )
                else:
                    self._current_token = self.con.render_text(
                        "path", self.prefs["color_path"]
                    )
            else:
                self._current_token = self.con.render_text(
                    "command", self.prefs["color_command"]
                )
            if (
                len(path_completions) == 1
                and not path_completions[0][-1] in [" ", "*"]
                and not self._current_node.get_node(path_completions[0]).children
            ):
                path_completions[0] = path_completions[0] + " "
            completions.extend(path_completions)
        else:
            self._current_token = self.con.render_text(
                "command", self.prefs["color_command"]
            )

        # Even a bookmark
        bookmarks = [
            "@" + bookmark
            for bookmark in self.prefs["bookmarks"]
            if bookmark.startswith("%s" % text.lstrip("@"))
        ]
        self.log.debug(f"Found bookmarks {str(bookmarks)}.")
        if bookmarks:
            completions.extend(bookmarks)

        # We are done
        return completions

    def _complete_token_path(self, text: str):
        """
        Completes a partial path token.
        @param text: Current text being typed by the user.
        @return: Possible completions for the token.
        @rtype: list of str
        """
        completions = []
        if text.endswith("."):
            text = text + "/"
        (basedir, slash, partial_name) = text.rpartition("/")
        self.log.debug(f"Got basedir={basedir}, partial_name={partial_name}")
        basedir = basedir + slash
        target = self._current_node.get_node(basedir, _async_load_=True)
        names = [child.name for child in target.children]

        # Iterall path completion
        if names and partial_name in ["", "*"]:
            # Not suggesting iterall to end a path that has only one
            # child allows for fast TAB action to add the only child's
            # name.
            if len(names) > 1:
                completions.append("%s* " % basedir)

        for name in names:
            num_matches = 0
            if name.startswith(partial_name):
                num_matches += 1
                if num_matches == 1:
                    completions.append(f"{basedir}{name}/")
                else:
                    completions.append(f"{basedir}{name}")

        # Bookmarks
        bookmarks = [
            "@" + bookmark
            for bookmark in self.prefs["bookmarks"]
            if bookmark.startswith("%s" % text.lstrip("@"))
        ]
        self.log.debug(f"Found bookmarks {str(bookmarks)}.")
        if bookmarks:
            completions.extend(bookmarks)

        if len(completions) == 1:
            self.log.debug("One completion left.")
            if not completions[0].endswith("* "):
                if not self._current_node.get_node(
                    completions[0], _async_load_=True
                ).children:
                    completions[0] = completions[0].rstrip("/") + " "

        self._current_token = self.con.render_text("path", self.prefs["color_path"])
        return completions

    def _complete_token_pparam(
        self,
        text: str,
        path: str,
        command: str,
        pparams: list[str],
        kparams: dict[str, str],
    ):
        """
        Completes a positional parameter token, which can also be the keywork
        part of a kparam token, as before the '=' sign is on the line, the
        parser cannot know better.
        @param path: Path of the target ConfigNode.
        @param command: The command (if any) found by the parser.
        @param pparams: Positional parameters from commandline.
        @param kparams: Keyword parameters from commandline.
        @param text: Current text being typed by the user.
        @return: Possible completions for the token.
        @rtype: list of str
        """
        completions = []
        target = self._current_node.get_node(path, _async_load_=True)
        cmd_params, free_pparams, free_kparams = target.get_command_signature(command)
        current_parameters = {}
        for index in range(len(pparams)):
            if index < len(cmd_params):
                current_parameters[cmd_params[index]] = pparams[index]
        for key, value in kparams.items():
            current_parameters[key] = value
        self._completion_help_topic = command
        completion_method = target.get_completion_method(command)
        self.log.debug(f"Command {command} accepts parameters {cmd_params}.")

        # Do we still accept positional params ?
        pparam_ok = True
        for index in range(len(cmd_params)):
            param = cmd_params[index]
            if param in kparams:
                if index <= len(pparams):
                    pparam_ok = False
                    self.log.debug("No more possible pparams (because of kparams).")
                    break
            elif (text.strip() == "" and len(pparams) == len(cmd_params)) or (
                len(pparams) > len(cmd_params)
            ):
                pparam_ok = False
                self.log.debug("No more possible pparams.")
                break
        else:
            if len(cmd_params) == 0:
                pparam_ok = False
                self.log.debug("No more possible pparams (none exists)")

        # If we do, find out which one we are completing
        if pparam_ok:
            if not text:
                pparam_index = len(pparams)
            else:
                pparam_index = len(pparams) - 1
            self._current_parameter = cmd_params[pparam_index]
            self.log.debug(f"Completing pparam {self._current_parameter}.")
            if completion_method:
                pparam_completions = completion_method(
                    current_parameters, text, self._current_parameter
                )
                if asyncio.iscoroutine(pparam_completions):
                    pparam_completions = self.run_async(pparam_completions)
                if pparam_completions is not None:
                    completions.extend(pparam_completions)

        # Add the keywords for parameters not already on the line
        if text:
            offset = 1
        else:
            offset = 0
        keyword_completions = [
            param + "="
            for param in cmd_params[len(pparams) - offset :]
            if param not in kparams
            if param.startswith(text)
        ]

        self.log.debug(f"Possible pparam values are {str(completions)}.")
        self.log.debug(f"Possible kparam keywords are{str(keyword_completions)}.")

        if keyword_completions:
            if self._current_parameter:
                self._current_token = (
                    self.con.render_text(
                        self._current_parameter, self.prefs["color_parameter"]
                    )
                    + "|"
                    + self.con.render_text("keyword=", self.prefs["color_keyword"])
                )
            else:
                self._current_token = self.con.render_text(
                    "keyword=", self.prefs["color_keyword"]
                )
        else:
            if self._current_parameter:
                self._current_token = self.con.render_text(
                    self._current_parameter, self.prefs["color_parameter"]
                )
            else:
                self._current_token = ""

        completions.extend(keyword_completions)

        if free_kparams or free_pparams:
            self.log.debug("Command has free [kp]params.")
            if completion_method:
                self.log.debug("Calling completion method for free params.")
                free_completions = completion_method(current_parameters, text, "*")
                if asyncio.iscoroutine(free_completions):
                    free_completions = self.run_async(free_completions)
                do_free_pparams = False
                do_free_kparams = False
                for free_completion in free_completions:
                    if free_completion.endswith("="):
                        do_free_kparams = True
                    else:
                        do_free_pparams = True

                if do_free_pparams:
                    self._current_token = (
                        self.con.render_text(
                            free_pparams, self.prefs["color_parameter"]
                        )
                        + "|"
                        + self._current_token
                    )
                    self._current_token = self._current_token.rstrip("|")
                    if not self._current_parameter:
                        self._current_parameter = "free_parameter"

                if do_free_kparams:
                    if not "keyword=" in self._current_token:
                        self._current_token = (
                            self.con.render_text(
                                "keyword=", self.prefs["color_keyword"]
                            )
                            + "|"
                            + self._current_token
                        )
                        self._current_token = self._current_token.rstrip("|")
                    if not self._current_parameter:
                        self._current_parameter = "free_parameter"

                completions.extend(free_completions)

        self.log.debug(f"Found completions {str(completions)}.")
        return completions

    def _complete_token_kparam(
        self,
        text: str,
        path: str,
        command: str,
        pparams: list[str],
        kparams: dict[str, str],
    ):
        """
        Completes a keyword=value parameter token.
        @param path: Path of the target ConfigNode.
        @param command: The command (if any) found by the parser.
        @param pparams: Positional parameters from commandline.
        @param kparams: Keyword parameters from commandline.
        @param text: Current text being typed by the user.
        @return: Possible completions for the token.
        @rtype: list of str
        """
        self.log.debug("Called for text='%s'" % text)
        target = self._current_node.get_node(path, _async_load_=True)
        cmd_params = target.get_command_signature(command)[0]
        self.log.debug(f"Command {command} accepts parameters {cmd_params}.")

        (keyword, sep, current_value) = text.partition("=")
        self.log.debug(f"Completing '{current_value}' for kparam {keyword}")

        self._current_parameter = keyword
        current_parameters = {}
        for index in range(len(pparams)):
            current_parameters[cmd_params[index]] = pparams[index]
        for key, value in kparams.items():
            current_parameters[key] = value
        completion_method = target.get_completion_method(command)
        completions = []
        if completion_method:
            completions = completion_method(current_parameters, current_value, keyword)
            if asyncio.iscoroutine(completions):
                completions = self.run_async(completions)
            if completions is None:
                completions = []

        self._current_token = self.con.render_text(
            self._current_parameter, self.prefs["color_parameter"]
        )

        self.log.debug("Found completions %s." % str(completions))

        return ["%s=%s" % (keyword, completion) for completion in completions]

    def _complete(self, text: str, state: int):
        """
        Text completion method, directly called by readline.
        Finds out what token the user wants completion for, and calls the
        _dispatch_completion() to get the possible completions.
        Then implements the state system needed by readline to return those
        possible completions to readline.
        @param text: The text to complete.
        @returns: The next possible completion for text.
        @rtype: str
        """
        if state == 0:
            cmdline = readline.get_line_buffer()
            self._current_completions = []
            self._completion_help_topic = ""
            self._current_parameter = ""

            (parse_results, path, command, pparams, kparams) = self._parse_cmdline(
                cmdline
            )

            beg = readline.get_begidx()
            end = readline.get_endidx()
            current_token = None

            if beg == end:
                # No text under the cursor, fake it so that the parser
                # result_trees gives us a token name on a second parser call
                self.log.debug("Faking text entry on commandline.")
                parse_results = self._parse_cmdline(cmdline + "x")[0]

                if parse_results.command.value == "x":
                    current_token = "command"
                elif "x" in [x.value for x in parse_results.pparams]:
                    current_token = "pparam"
                elif "x" in [x.value for x in parse_results.kparams]:
                    current_token = "kparam"
            elif path and beg == parse_results.path.locn_start:
                current_token = "path"
            elif command and beg == parse_results.command.locn_start:
                current_token = "command"
            elif pparams and beg in [p.locn_start for p in parse_results.pparams]:
                current_token = "pparam"
            elif kparams and beg in [k.locn_start for k in parse_results.kparams]:
                current_token = "kparam"

            self._current_completions = self._dispatch_completion(
                path, command, pparams, kparams, text, current_token
            )

            self.log.debug(
                f"Returning completions {str(self._current_completions)} to readline."
            )

        if state < len(self._current_completions):
            return self._current_completions[state]
        else:
            return None

    def _dispatch_completion(
        self,
        path: str,
        command: str,
        pparams: list[str],
        kparams: dict[str, str],
        text: str,
        current_token: str,
    ) -> list[str]:
        """
        This method takes care of dispatching the current completion request
        from readline (via the _complete() method) to the relevant token
        completion methods. It has to cope with the fact that the commandline
        being incomplete yet,
        Of course, as the command line is still unfinished, the parser can
        only do so much of a job. For instance, until the '=' sign is on the
        command line, there is no way to distinguish a positional parameter
        from the begining of a keyword=value parameter.
        @param path: Path of the target ConfigNode.
        @param command: The command (if any) found by the parser.
        @param pparams: Positional parameters from commandline.
        @param kparams: Keyword parameters from commandline.
        @param text: Current text being typed by the user.
        @param current_token: Name of token to complete.
        @return: Possible completions for the token.
        @rtype: list of str
        """
        completions = []

        self.log.debug(
            f"Dispatching completion for '{current_token}' token. "
            f"text={text}, path={path}, command={command}, "
            f"pparams={str(pparams)}, kparams={str(kparams)}"
        )

        (path, iterall) = path.partition("*")[:2]
        if iterall:
            cpl_path = path
            try:
                target = self._current_node.get_node(path, _async_load_=True)
            except ValueError:
                pass
            else:
                children = target.children
                if children:
                    cpl_path = list(children)[0].path
        else:
            cpl_path = path

        if current_token == "command":
            completions = self._complete_token_command(text, cpl_path, command)
        elif current_token == "path":
            completions = self._complete_token_path(text)
        elif current_token == "pparam":
            completions = self._complete_token_pparam(
                text, cpl_path, command, pparams, kparams
            )
        elif current_token == "kparam":
            completions = self._complete_token_kparam(
                text, cpl_path, command, pparams, kparams
            )
        else:
            self.log.debug(f"Cannot complete unknown token {current_token}.")

        return completions

    def _get_prompt(self):
        """
        Returns the command prompt string.
        """
        prompt_path = self._current_node.path
        prompt_length = self.prefs["prompt_length"]

        if prompt_length and prompt_length < len(prompt_path):
            half = (prompt_length - 3) // 2
            prompt_path = f"{prompt_path[:half]}...{prompt_path[-half:]}"

        _msg = self._current_node.prompt_msg()
        if _msg == "" or prompt_path == "/":
            return f"{prompt_path}>"
        return f"{prompt_path} \n{_msg}> "

    def _cli_loop(self):
        """
        Starts the configuration shell interactive loop, that:
            - Goes to the last current path
            - Displays the prompt
            - Waits for user input
            - Runs user command
        """
        while not self._exit:
            try:
                readline.parse_and_bind("tab: complete")
                readline.set_completer(self._complete)
                cmdline = input(self._get_prompt()).strip()
            except EOFError:
                self.con.raw_write("exit\n")
                cmdline = "exit"
            self.run_cmdline(cmdline)
            if self._save_history:
                try:
                    readline.write_history_file(self._cmd_history)
                except IOError:
                    self.log.warning(
                        f"Cannot write to command history file {self._cmd_history}."
                    )
                    self.log.warning("Saving command history has been disabled!")
                    self._save_history = False

    def _parse_cmdline(self, line: str):
        """
        Parses the command line entered by the user. This is a wrapper around
        the actual pyparsing parser that pre-chews the result trees to
        cleanly extract the tokens we care for (parameters, path, command).
        @param line: The command line to parse.
        @return: (result_trees, path, command, pparams, kparams),
        pparams being positional parameters and kparams the keyword=value.
        @rtype: (pyparsing.ParseResults, str, str, list, dict)
        """
        self.log.debug("Parsing commandline.")
        path = ""
        command = ""
        pparams = []
        kparams = {}

        parse_results = self._parser.parseString(line)
        self.log.debug(parse_results)
        if isinstance(parse_results.path, ParseResults):
            path = parse_results.path.value
        if isinstance(parse_results.command, ParseResults):
            command = parse_results.command.value
        if isinstance(parse_results.pparams, ParseResults):
            pparams = [pparam.value for pparam in parse_results.pparams]
        if isinstance(parse_results.kparams, ParseResults):
            kparams = dict([kparam.value for kparam in parse_results.kparams])

        self.log.debug(
            f"Parse gave path={path} command={command} pparams={str(pparams)} kparams={str(kparams)}"
        )
        return parse_results, path, command, pparams, kparams

    def _execute_command(
        self, path: str, command: str, pparams: list[str], kparams: dict[str, str]
    ):
        """
        Calls the target node to execute a command.
        Behavior depends on the target node command's result:
            - An 'EXIT' string will trigger shell exit.
            - None will do nothing.
            - A ConfigNode object will trigger a current_node change.
        @param path: Path of the target node.
        @param command: The command to call.
        @param pparams: The positional parameters to use.
        @param kparams: The keyword=value parameters to use.
        """
        if path.endswith("*"):
            path = path.rstrip("*")
            iterall = True
        else:
            iterall = False

        if not path:
            path = "."

        if not command:
            if iterall:
                command = "ls"
            else:
                command = "cd"
                pparams = ["."]

        try:
            target = self._current_node.get_node(path, _async_load_=True)
        except ValueError as msg:
            raise Exception(str(msg))

        result = None
        if not iterall:
            targets = [target]
        else:
            targets = target.children
        for target in targets:
            if iterall:
                self.con.display(f"[{target.path}]")
            try:
                result = target.execute_command(command, pparams, kparams)
            except Exception as e:
                self.log.exception("Internal error")
                return
        self.log.debug(f"Command execution returned {result}")
        if isinstance(result, ConfigNode):
            self._current_node = result
        elif result == "EXIT":
            self._exit = True
        elif result is not None:
            self.log.error(f"Unexpected result: {result}")

    # Public methods

    def run_async(self, cor: Coroutine):
        return self.loop.run_until_complete(cor)

    def run_cmdline(self, cmdline: str):
        """
        Runs the specified command. Global commands are checked first,
        then local commands from the current node.

        Command syntax is:
        [PATH] COMMAND [POSITIONAL_PARAMETER]+ [PARAMETER=VALUE]+

        @param cmdline: The command line to run
        """
        if cmdline:
            self.log.verbose(f"Running command line {cmdline}.")
            path, command, pparams, kparams = self._parse_cmdline(cmdline)[1:]
            self._execute_command(path, command, pparams, kparams)

    def run_script(self, script_path: str, exit_on_error: bool = True):
        """
        Runs the script located at script_path.
        Script runs always start from the root context.
        @param script_path: File path or TextIO of the script to run
        @param exit_on_error: If True, stops the run if an error occurs
        """
        script_fd = None
        try:
            script_path = os.path.expanduser(script_path)
            script_fd = open(script_path, "r")
            self.run_stdin(script_fd, exit_on_error)
        except IOError as msg:
            raise IOError(msg)
        finally:
            if script_fd is not None:
                script_fd.close()

    def run_stdin(
        self,
        file_descriptor: TextIO | list[str] = sys.stdin,
        exit_on_error: bool = True,
    ):
        """
        Reads commands to be run from a file descriptor, stdin by default.
        The run always starts from the root context.
        @param file_descriptor: The file descriptor to read commands from
        @param exit_on_error: If True, stops the run if an error occurs
        """
        self._current_node = self._root_node
        for cmdline in file_descriptor:
            try:
                self.run_cmdline(cmdline.strip())
            except Exception as msg:
                self.log.exception(msg)
                if exit_on_error is True:
                    raise ExecutionError("Aborting run on error.")

                self.log.exception("Keep running after an error.")

    def run_interactive(self):
        """
        Starts interactive CLI mode.
        """
        history = self.prefs["path_history"]
        index = self.prefs["path_history_index"]
        if history and index:
            if index < len(history):
                try:
                    target = self._root_node.get_node(history[index], _async_load_=True)
                except ValueError:
                    self._current_node = self._root_node
                else:
                    self._current_node = target

        while True:
            old_completer = None
            try:
                old_completer = readline.get_completer()
                self._cli_loop()
                break
            except KeyboardInterrupt:
                self.con.raw_write("\n")
            except ExecutionError as e:
                self.log.exception(e)
                self.con.raw_write("\n")
            finally:
                if old_completer is not None:
                    readline.set_completer(old_completer)

    def attach_root_node(self, root_node: ConfigNode):
        """
        @param root_node: The root ConfigNode object
        """
        self._current_node = root_node
        self._root_node = root_node
