import time

from configshell_fb import Log as ConfigShellLog
from pathlib import Path


class Log(ConfigShellLog):

    def _append(self, msg, level):
        date_fields = time.localtime()
        date = "%d-%02d-%02d %02d:%02d:%02d" % (
            date_fields[0],
            date_fields[1],
            date_fields[2],
            date_fields[3],
            date_fields[4],
            date_fields[5],
        )

        with Path(self.prefs["logfile"]).open(mode="a") as f:
            f.write(f"[{level}] {date} {msg}\n")
