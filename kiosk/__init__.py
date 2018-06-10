import curses

class MenuManager:
    def __init__(self, win, start_menu):
        self._win = win
        self._menu_stack = []
        self._current_menu = None
        self.change_menu(start_menu)

    def __bool__(self):
        return bool(self._current_menu)

    def change_menu(self, menu, replace=False):
        if self._current_menu:
            self._current_menu.exit()
            if not replace:
                self._menu_stack.append(self._current_menu)
        self._current_menu = menu
        self._current_menu._mm = self
        self._current_menu.open(self._win)
        self._current_menu.resize(self._win.getmaxyx())

    def pop_menu(self):
        if self._menu_stack:
            self.change_menu(self._menu_stack.pop(), True)
        else:
            self._current_menu.exit()
            self._current_menu = None

    def draw(self):
        self._current_menu.draw(self._win)

    def ch(self, c):
        if c == curses.KEY_RESIZE:
            self._current_menu.resize(self._win.getmaxyx())
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            self._current_menu.select()
        elif c == curses.KEY_BACKSPACE and not self._current_menu.back():
            self.pop_menu()
            return
        self._current_menu.ch(c)


class BaseMenu:
    def __init__(self):
        self._mm = None
        pass

    def open(self, win):
        pass

    def draw(self, win):
        pass

    def ch(self, c):
        pass

    def resize(self, size):
        pass

    def select(self):
        pass

    def back(self):
        pass

    def exit(self):
        pass

class SelectMenu(BaseMenu):
    def __init__(self, title):
        self._title = title
        self._entries = []
        self._size = (0, 0)
        self._offset = 0
        self._length = 0
        self._cursor = 0

    def set_entries(self, entries):
        self._entries = entries

    def current_entry(self):
        return self._entries[self._cursor] if self._length else None

    def draw(self, win):
        win.addstr(1, 1, self._title)
        for i in range(self._offset, min(self._offset + self._length, len(self._entries))):
            if i == self._cursor:
                win.addstr(3 + i - self._offset, 1, str(self._entries[i]), curses.A_REVERSE)
            else:
                win.addstr(3 + i - self._offset, 1, str(self._entries[i]))
        if self._entries:
            win.addstr(self._size[0] - 2, 1, '{} / {} '.format(self._cursor + 1, len(self._entries)))
        else:
            win.addstr(self._size[0] - 2, 1, '0 / 0 ')

    def ch(self, c):
        if not self._entries:
            self._cursor = 0
        elif c == curses.KEY_UP:
            self._cursor -= 1
            if self._cursor < 0:
                self._cursor = len(self._entries) - 1
        elif c == curses.KEY_DOWN:
            self._cursor = (self._cursor + 1)%len(self._entries)
        pad = 2 if self._length > 5 else 0
        if self._cursor < self._offset + pad:
            self._offset = self._cursor - pad
            if self._offset < 0:
                self._offset = 0
        elif self._cursor > self._offset + self._length - pad - 1:
            self._offset = self._cursor - self._length + pad + 1

    def resize(self, size):
        self._size = size
        self._length = max(0, size[0] - 6)
