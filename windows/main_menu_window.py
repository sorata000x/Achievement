from .config import *
from .achievement_menu_window import AchievementMenuWindow
from widgets.menu_button import MenuButtonWidget
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QToolButton


class MainMenuWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        # Window config
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # set background transparent
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # Background
        self.background = QWidget(self)
        self.background.resize(self.size())
        self.background.setObjectName("panel")
        # Sub windows
        self.achievement_menu = AchievementMenuWindow()
        # Tool Buttons
        self.buttons_container = QWidget(self.background)
        self.buttons_container.resize(self.width(), 270)
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setContentsMargins(3, 0, 3, 0)
        self.buttons_layout.setSpacing(12)
        self.menu_buttons = {
            "achievement": MenuButtonWidget("ACHIEVEMENT"),
            "skill_tree": MenuButtonWidget("SKILL TREE"),
            "experience": MenuButtonWidget("EXPERIENCE", has_toggle=True),
            "quest": MenuButtonWidget("QUEST"),
            "quit": MenuButtonWidget("QUIT"),     # DEBUG
        }
        for key, value in self.menu_buttons.items():
            self.buttons_layout.addWidget(value)
        self.menu_buttons["achievement"].clicked.connect(self.achievement_menu.show)

        #   DEBUG
        self.menu_buttons["quit"].clicked.connect(app.quit)
        self.buttons_container.setLayout(self.buttons_layout)
        #   Tools
        self.setting_button = QToolButton(self.background)
        self.setting_button.move(4, 268)
        self.user_button = QToolButton(self.background)
        self.user_button.move(200, 268)

    def move(self, x, y):
        """ Move sub-windows_ol as well."""
        super().move(x, y)
        self.achievement_menu.move(x, y)
