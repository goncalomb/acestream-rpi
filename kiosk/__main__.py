import curses

from . import MenuManager, arenavision

class WrappedWindow():
    def __init__(self, instance):
        self._instance = instance

    def __getattr__(self, name):
        return getattr(self._instance, name)

    def addstr(self, y, x, strr, attr=0):
        size = self.getmaxyx()
        if y < size[0] - 1 and x < size[1] - 1:
            self.addnstr(y, x, strr, size[1] - x - 1, attr)

def main(stdscr):
    # wrap window instance to make addstr safer (no overflow)
    stdscr = WrappedWindow(stdscr)
    stdscr.timeout(1000)

    mm = MenuManager(stdscr, arenavision.Menu())
    while mm:
        mm.draw()
        c = stdscr.getch()
        stdscr.erase()
        mm.ch(c)

    stdscr.clear()
    stdscr.refresh()

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
