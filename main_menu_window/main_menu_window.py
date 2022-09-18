from PyQt6.QtGui import QFontDatabase

from .config import *

from main_menu_window.widgets.menu_button import MenuButtonWidget
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QToolButton, QLabel

from .functions import getFont
from .pages.ach_menu_page.ach_menu_page import AchievementMenuPage
from .widgets.h_line import QHLine


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        # Window Config
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # set background transparent
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # Elements
        # --- Background
        self.background = QWidget(self)
        self.background.resize(self.size())
        self.background.setObjectName("panel")
        # --- Menu Label
        self.menu_label = QLabel("Menu", self)
        self.menu_label.setStyleSheet("""font-size: 28pt; color: #cfcfcf;""")
        self.menu_label.setFont(getFont("roboto/Roboto-Thin.ttf"))
        self.menu_label.move(90, 30)
        # --- Horizontal Line
        self.h_line = QHLine(self)
        self.h_line.setStyleSheet("""border: 1px solid #cfcfcf;""")
        self.h_line.resize(self.width()-20, 1)
        self.h_line.move(10, 62)
        # --- Tool Buttons
        # ------ Container for tool buttons layout
        self.tb_container = QWidget(self.background)
        self.tb_container.resize(self.width(), 280)
        self.tb_container.move(0, 73)
        # ------ Layout for tool buttons
        self.tb_layout = QVBoxLayout()
        self.tb_layout.setContentsMargins(14, 0, 14, 0)
        self.tb_layout.setSpacing(6)
        # ------ Tool buttons
        self.menu_buttons = {
            "achievement": MenuButtonWidget("ACHIEVEMENT"),
            "skill_tree": MenuButtonWidget("SKILL TREE"),
            "experience": MenuButtonWidget("EXPERIENCE", has_toggle=True),
            "quest": MenuButtonWidget("QUEST"),
            "quit": MenuButtonWidget("QUIT"),  # DEBUG
        }
        for name, widget in self.menu_buttons.items():
            self.tb_layout.addWidget(widget)
# DEBUG; gotta move to somewhere else eventually
        self.menu_buttons["quit"].clicked.connect(app.quit)
        self.tb_container.setLayout(self.tb_layout)
# -----
        # --- Other Tools
        # ------ Setting button
        self.setting_button = QToolButton(self.background)
        self.setting_button.move(10, 366)
        self.setting_button.clicked.connect(self.setting_button.hide)
        # ------ User button
        self.user_button = QToolButton(self.background)
        self.user_button.move(224, 366)
        # Pages
        # --- Achievement Menu Page
        self.achievement_menu = AchievementMenuPage(self)
        self.achievement_menu.hide()
        self.menu_buttons["achievement"].clicked.connect(self.achievement_menu.show)

    def move(self, x, y):
        """ Move sub-main_menu_window as well."""
        super().move(x, y)