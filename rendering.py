
LINE_NORMAL = 0
LINE_HIGHLIGHT = 1
LINE_TITLE = 2

MENU_PAGE_SIZE = 25
MENU_RENDER_TYPE = 0

class LineItem:
    def __init__(self, title="", line_type=LINE_NORMAL, show_arrow=False):
        self.title = title
        self.line_type = line_type
        self.show_arrow = show_arrow

class Rendering:
    def __init__(self, type):
        self.type = type

    def unsubscribe(self):
        pass


class MenuRendering(Rendering):
    def __init__(self, header="", lines=[], page_start=0, total_count=0):
        super().__init__(MENU_RENDER_TYPE)
        self.lines = lines
        self.header = header
        self.page_start = page_start
        self.total_count = total_count
        self.now_playing = "playing"
        self.has_internet = True
