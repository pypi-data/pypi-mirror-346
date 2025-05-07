from __future__ import annotations

from typing import TYPE_CHECKING

from ..exception import ExecutionError

if TYPE_CHECKING:
    from configshell_fb import ConfigNode


class CmdHelp:
    def ui_command_help(self: ConfigNode, topic: str = None):
        """
        Displays the manual page for a topic, or list available topics.
        """
        commands = self.list_commands()
        if topic is None:
            msg = self.shell.con.dedent(self.help_intro)
            msg += self.shell.con.dedent(
                """

                                   AVAILABLE COMMANDS
                                   ==================
                                   The following commands are available in the
                                   current path:

                                   """
            )
            for command in commands:
                msg += "  - %s\n" % self.get_command_syntax(command)[0]
            msg += "\n"
            self.shell.con.epy_write(msg)
            return

        if topic not in commands:
            raise ExecutionError("Cannot find help topic %s." % topic)

        syntax, comments, defaults = self.get_command_syntax(topic)
        msg = self.shell.con.dedent(
            """
                             SYNTAX
                             ======
                             %s

                             """
            % syntax
        )
        for comment in comments:
            msg += comment + "\n"

        if defaults:
            msg += self.shell.con.dedent(
                """
                                  DEFAULT VALUES
                                  ==============
                                  %s

                                  """
                % defaults
            )
        msg += self.shell.con.dedent(
            """
                              DESCRIPTION
                              ===========
                              """
        )
        msg += self.get_command_description(topic)
        msg += "\n"
        self.shell.con.epy_write(msg)

    def ui_complete_help(
        self: ConfigNode, parameters: dict[str, str], text: str, current_param: str
    ):
        """
        Parameter auto-completion method for user command help.
        @param parameters: Parameters on the command line.
        @param text: Current text of parameter being typed by the user.
        @param current_param: Name of parameter to complete.
        @return: Possible completions
        @rtype: list of str
        """
        if current_param == "topic":
            # TODO Add other types of topics
            topics = self.list_commands()
            completions = [topic for topic in topics if topic.startswith(text)]
        else:
            completions = []

        if len(completions) == 1:
            return [completions[0] + " "]
        else:
            return completions
