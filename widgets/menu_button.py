from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QLabel

from widgets.toggle import ToggleWidget
from functions import *

class MenuButtonWidget(QPushButton):
    def __init__(self, title="", parent=None, has_toggle=False):
        super().__init__(parent)
        # config
        self.setObjectName("menu_button")
        # title
        self.title = QLabel(title, self)
        self.title.setFont(getFont('LeagueGothic-Regular.otf'))
        self.title.move(43, 6)
        self.title.setObjectName("menu_button_title")
        # icon
        self.setIcon(QIcon("images/trophy_icon.png"))
        self.setIconSize(QSize(28, 28))
        # toggle
        if has_toggle:
            self.toggle = ToggleWidget(self)
            self.toggle.move(200, 13)
