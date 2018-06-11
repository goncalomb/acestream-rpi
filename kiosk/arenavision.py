import curses, requests, lxml.html, re

from . import SelectMenu
from .acestream import OpenStreamMenu

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

class Menu(SelectMenu):
    def __init__(self):
        super().__init__('Arena Vision Streams')

    def open(self, win):
        win.addstr(1, 1, 'LOADING', curses.A_REVERSE)
        win.refresh()
        self.set_entries(get_arena_vision_streams())
        win.erase()

    def select(self):
        e = self.current_entry()
        if e:
            self._mm.change_menu(OpenStreamMenu(e.get_hash()))
