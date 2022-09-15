from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtWidgets import QPushButton, QLabel

from main_menu_window.widgets.toggle import ToggleWidget
from main_menu_window.functions import *

class MenuButtonWidget(QPushButton):
    def __init__(self, title="", parent=None, has_toggle=False):
        super().__init__(parent)
        # config
        self.setObjectName("menu_button")
        # Element
        # --- title
        self.title = QLabel(title, self)
        self.title.setFont(getFont('LeagueGothic-Regular.otf'))
        self.title.move(43, 6)
        #self.title.setObjectName("menu_button_title")
        self.title.setStyleSheet("color: #ffffff;")
        # --- icon
        self.setIcon(QIcon("images/trophy_icon.png"))
        self.setIconSize(QSize(28, 28))
        # --- toggle
        if has_toggle:
            self.toggle = ToggleWidget(self)
            self.toggle.move(186, 13)
        # Effect
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
