import subprocess
import os, signal

from . import config, BaseMenu

def start_acestream_player(h):
    return subprocess.Popen(
        [arg.format(hash=h) for arg in config.aceplayer_command],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        preexec_fn=os.setpgrp
    )

class OpenStreamMenu(BaseMenu):
    def __init__(self, h):
        self._proc = start_acestream_player(h)

    def draw(self, win):
        win.addstr(1, 1, 'PLAYING ACESTREAM ')

    def ch(self, c):
        if not self._proc or self._proc.poll():
            self._mm.pop_menu()

    def exit(self):
        try:
            os.killpg(self._proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        self._proc.terminate()
        self._proc.wait()
