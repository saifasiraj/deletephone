from music import *
from settings import *

LARGEFONT = ("ChicagoFLF", 90)
MED_FONT = ("ChicagoFLF", 70)
SCALE = 1
SPOT_GREEN = "#1DB954"
SPOT_BLACK = "#191414"
SPOT_WHITE = "#FFFFFF"
class RootPage(MenuPage):
    def __init__(self, previous_page):
        super().__init__("", previous_page, has_sub_page=True)
        self.pages = [MusicPage(self),
                      SettingsPage(self)]
        self.index = 0
        self.page_start = 0

    def get_pages(self):
        return self.pages

    def total_size(self):
        return len(self.get_pages())

    def page_at(self, index):
        return self.get_pages()[index]
