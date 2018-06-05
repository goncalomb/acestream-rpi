#!/usr/bin/env python3

import curses, requests, lxml.html, re, subprocess

player_proc = None

def stream_play(h):
    global player_proc
    stream_stop()
    player_proc = subprocess.Popen(['/bin/bash', './play.sh', h], close_fds=True)

def stream_stop():
    global player_proc
    if player_proc:
        player_proc.kill()
        player_proc.send_signal(subprocess.signal.SIGKILL)
        player_proc = None
        return True
    player_proc = None
    return False

class ArenaVisionStream:

    def __init__(self, url, name):
        self._url = url
        self._hash = None
        self.name = name

    def get_hash(self):
        if not self._hash:
            r = requests.get(self._url, cookies={
                'beget': 'begetok' # cloudflare cookie
            })
            if r.status_code == 200:
                doc = lxml.html.fromstring(r.content)
                href = doc.cssselect('p.auto-style1 a')[0].get('href')
                self._hash = re.match('acestream://([0-9a-f]{40})', href, re.IGNORECASE).group(1)
        return self._hash

    def __str__(self):
        return self.name

def get_arena_vision_streams():
    re_av_title = re.compile('ArenaVision\\s+(\\d+)')
    re_streams = re.compile('(\\d+)\\s*(?:-\\s*(\\d+)\\s*)?\\[(\\w+)\\]')

    def parse_stream_langs(s):
        for m in re_streams.finditer(s):
            g1 = m.group(1)
            g2 = m.group(2)
            g3 = m.group(3)
            if g2:
                for i in range(int(g1), int(g2) + 1):
                    yield (i, g3)
            else:
                yield (int(g1), g3)

    r = requests.get('http://arenavision.in/guide', cookies={
        'beget': 'begetok' # cloudflare cookie
    })
    if r.status_code == 200:
        doc = lxml.html.fromstring(r.content)
        data = []
        stream_urls = {}
        for a in doc.cssselect('ul.menu li.leaf a'):
            m = re_av_title.match(a.text_content())
            if m:
                stream_urls[int(m.group(1))] = str(a.get('href'))
        for tr in doc.xpath('//table[@class="auto-style1"]/tr'):
            tds = tr.getchildren()
            if len(tds) == 6:
                name = tds[0].text_content()[:5] + ' ' + tds[1].text_content()[:5] + ' ' + tds[2].text_content().strip() + ' ' + tds[4].text_content()
                for n, lang in parse_stream_langs(tds[5].text_content()):
                    data.append(ArenaVisionStream(stream_urls[n], name + ' (' + lang + ', ' + str(n) + ')'))
        return data
    return None


def main(stdscr):
    size = (0, 0)

    menu_off = 0
    menu_len = 5
    menu_cur = 0

    def handle_size():
        nonlocal size, menu_len
        size = stdscr.getmaxyx()
        menu_len = max(0, size[0] - 6)

    handle_size()

    def safe_addstr(y, x, strr, attr=0):
        if y < size[0] - 1 and x < size[1] - 1:
            stdscr.addnstr(y, x, strr, size[1] - x - 1, attr)

    # get menu data
    safe_addstr(1, 1, 'LOADING', curses.A_REVERSE)
    stdscr.refresh()
    data = get_arena_vision_streams()

    # menu loop
    while True:
        safe_addstr(1, 1, 'Arena Vision Streams')
        for i in range(menu_off, min(menu_off + menu_len, len(data))):
            if i == menu_cur:
                safe_addstr(3 + i - menu_off, 1, str(data[i]), curses.A_REVERSE)
            else:
                safe_addstr(3 + i - menu_off, 1, str(data[i]))
        safe_addstr(size[0] - 2, 1, '{} / {} '.format(menu_cur + 1, len(data)))

        c = stdscr.getch()
        stdscr.erase()
        if c == curses.KEY_BACKSPACE:
            if not stream_stop():
                break
            else:
                safe_addstr(size[0] - 2, 10, 'KILLING PLAYER', curses.A_REVERSE)
                stdscr.refresh()
        elif c == curses.KEY_RESIZE:
            handle_size()
        elif c == curses.KEY_UP:
            menu_cur -= 1
            if menu_cur < 0:
                menu_cur = len(data) - 1
        elif c == curses.KEY_DOWN:
            menu_cur = (menu_cur + 1)%len(data)
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            stream_play(data[menu_cur].get_hash())

        pad = 2 if menu_len > 5 else 0
        if menu_cur < menu_off + pad:
            menu_off = menu_cur - pad
            if menu_off < 0:
                menu_off = 0
        elif menu_cur > menu_off + menu_len - pad - 1:
            menu_off = menu_cur - menu_len + pad + 1

    stdscr.clear()
    stdscr.refresh()

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
