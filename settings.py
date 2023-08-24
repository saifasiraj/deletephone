from menu import *


class SettingsPage(MenuPage):
    def __init__(self, previous_page):
        super().__init__("Settings", previous_page, has_sub_page=True)

    def total_size(self):
        return 5
