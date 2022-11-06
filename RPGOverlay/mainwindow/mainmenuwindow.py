from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QToolButton, QLabel

from ..components.menubutton import MenuButtonWidget
from config import *
from ..functions import getFont
from .pages.objectivemenupage import AchievementMenuPage
from ..components.hline import QHLine


class MainWindow(QMainWindow):
    def __init__(self, app, settings):
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
        self.menu_label.setStyleSheet("""font-size: 28pt; color: #dbdbdb;""")
        self.menu_label.setFont(getFont("roboto/Roboto-Thin.ttf"))
        self.menu_label.move(82, 30)
        # --- Horizontal Line
        self.h_line = QHLine(self)
        self.h_line.setStyleSheet("""border: 1px solid #dbdbdb;""")
        self.h_line.resize(self.width(), 1)
        self.h_line.move(0, 62)
        # --- Tool Buttons
        # ------ Container for tool buttons layout
        self.tb_container = QWidget(self.background)
        self.tb_container.resize(self.width(), 280)
        self.tb_container.move(0, 60)
        # ------ Layout for tool buttons
        self.tb_layout = QVBoxLayout()
        self.tb_layout.setContentsMargins(0, 0, 0, 0)     # 14, 0, 14, 0
        self.tb_layout.setSpacing(6)
        # ------ Tool buttons
        self.menu_buttons = {
            "achievement": MenuButtonWidget("ACHIEVEMENT"),
            "skill_tree": MenuButtonWidget("?????"),
            "experience": MenuButtonWidget("?????", has_toggle=True),
            "quest": MenuButtonWidget("?????"),
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
        self.setting_button.move(10, self.height()-34)
        self.setting_button.clicked.connect(self.setting_button.hide)
        # ------ User button
        self.user_button = QToolButton(self.background)
        self.user_button.move(204, self.height()-34)
        # Pages
        # --- Achievement Menu Page
        self.achievement_menu = AchievementMenuPage(settings, self)
        self.achievement_menu.hide()
        self.menu_buttons["achievement"].clicked.connect(self.achievement_menu.show)

    def move(self, x, y):
        """ Move sub-main_menu_window as well."""
        super().move(x, y)