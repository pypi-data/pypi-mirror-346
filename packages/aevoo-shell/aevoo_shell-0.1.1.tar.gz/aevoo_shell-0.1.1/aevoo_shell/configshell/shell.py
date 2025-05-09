from configshell import ConfigShell
from pyparsing import (
    OneOrMore,
    Optional,
    Regex,
    Suppress,
    Word,
    alphanums,
    locatedExpr,
    quotedString,
    removeQuotes,
)

from .log import Log


class Shell(ConfigShell):
    def __init__(self, preferences_dir=None):
        super().__init__(preferences_dir)

        # Grammar of the command line
        command = locatedExpr(Word(alphanums + "_"))("command")
        var = Word(alphanums + r"?;&*$!#,=_\+/.<>()~@:-%[]")
        value = quotedString.setParseAction(removeQuotes) | var
        keyword = Word(alphanums + r"_\-")
        kparam = locatedExpr(keyword + Suppress("=") + Optional(value, default=""))(
            "kparams*"
        )
        pparam = locatedExpr(var)("pparams*")
        parameter = kparam | pparam
        parameters = OneOrMore(parameter)
        bookmark = Regex("@([A-Za-z0-9:_.]|-)+")
        pathstd = (
            Regex(r"([A-Za-z0-9:_.\[\]@]|-)*" + "/" + r"([A-Za-z0-9:_.\[\]@/]|-)*")
            | ".."
            | "."
        )
        path = locatedExpr(bookmark | pathstd | "*")("path")
        parser = Optional(path) + Optional(command) + Optional(parameters)
        self._parser = parser
        self.log = Log()
