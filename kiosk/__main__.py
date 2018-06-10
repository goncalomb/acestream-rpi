import curses

from . import arenavision

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

    menu_stack = []

    current_menu = arenavision.Menu()
    current_menu.open(stdscr)
    current_menu.resize(stdscr.getmaxyx())

    while True:
        current_menu.draw(stdscr)
        c = stdscr.getch()
        stdscr.erase()
        if c == curses.KEY_RESIZE:
            current_menu.resize(stdscr.getmaxyx())
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            current_menu.select()
        elif c == curses.KEY_BACKSPACE:
            if not current_menu.back():
                current_menu.exit()
                if len(menu_stack):
                    current_menu = menu_stack.pop()
                    current_menu.open(stdscr)
                    current_menu.resize(stdscr.getmaxyx())
                    continue
                else:
                    break
        current_menu.ch(c)

    stdscr.clear()
    stdscr.refresh()

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
