import os.path

import argparse
import asyncio

from aevoo_pycontrol import Context
from aevoo_shell.configshell.shell import Shell
from .root import Root

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--profil", default="default", help="profil")

args = parser.parse_args()

_config_path = os.path.expanduser("~/.config/aevoo/shell")

_BANNER = r"""
                                           _          _ _ 
      __ _  _____   _____   ___        ___| |__   ___| | |
     / _` |/ _ \ \ / / _ \ / _ \ _____/ __| '_ \ / _ \ | |
    | (_| |  __/\ V / (_) | (_) |_____\__ \ | | |  __/ | |
     \__,_|\___| \_/ \___/ \___/      |___/_| |_|\___|_|_|

"""


def main():
    # pyfiglet.figlet_format("aevoo-shell")
    print(_BANNER)
    ctx = Context()
    asyncio.run(ctx.connect(args.profil))
    _shell = Shell(_config_path)
    root_ = Root(ctx=ctx, name="/", _shell=_shell)
    root_.load()
    _shell.run_interactive()


def test():
    ctx = Context()
    _shell = Shell(_config_path)
    root_ = Root(ctx=ctx, name="/", _shell=_shell)
    _shell.run_script(f"{_config_path}/test.script")
