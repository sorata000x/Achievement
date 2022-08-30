"""
    Objective: For RPGOverlay; To have system tray with window right below it.
    Current:
        - Icon tray & menu with utilities buttons and achievement menu
    To Do:
        - Create new achievement page
        - Add setting and user button at the end of menus to have better measure of the
size of the menus.
        - Add entries of create achievement page and button to add created achievement to menu.
        - Draw icons
            - Back button Icon
            - Skill Tree Icon
            - Experience Icon
            - Quest Icon
        - Button hover effect
"""

import sys
import os
from PyQt6.QtCore import Qt, QSize, QDir, QPropertyAnimation, QPoint, QEasingCurve
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from stylesheet import StyleSheet

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

font_id = QFontDatabase.addApplicationFont(f"{os.path.dirname(__file__)}/LeagueGothic-Regular.otf")
try:
    if font_id > -1:
        font_name = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_name, 34)
    else:
        raise Exception()
except Exception:
    print("Font file not found.")
    exit()

app.setStyleSheet(StyleSheet)

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(QIcon("icon.jpg"))
tray.setVisible(True)

def show_menu():
    if main_menu.isHidden():
        main_menu.move(tray.geometry().bottomLeft().x(), tray.geometry().bottomLeft().y()+5)
        main_menu.show()
    else:
        main_menu.hide()
    return

class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Window config
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # set background transparent
        self.resize(230, 268)
        # Panel
        self.panel = QWidget(self)
        self.panel.resize(self.size())
        self.panel.setStyleSheet("border-radius: 5px; background-color: white;")
        # Sub windows
        self.achievement_menu = AchievementMenuWindow()
        # Buttons
        self.buttons = QWidget()
        self.setCentralWidget(self.buttons)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(3, 0, 3, 0)
        self.layout.setSpacing(12)
        self.menu_buttons = {
            "achievement": MenuButtonWidget("ACHIEVEMENT"),
            "skill_tree": MenuButtonWidget("SKILL TREE"),
            "experience": MenuButtonWidget("EXPERIENCE", has_toggle=True),
            "quest": MenuButtonWidget("QUEST"),
            "quit": MenuButtonWidget("QUIT"),     # DEBUG
        }
        for key, value in self.menu_buttons.items():
            self.layout.addWidget(value)
        self.menu_buttons["achievement"].clicked.connect(self.achievement_menu.show)
        # DEBUG
        self.menu_buttons["quit"].clicked.connect(app.quit)
        self.buttons.setLayout(self.layout)

    def move(self, x, y):
        super().move(x, y)
        self.achievement_menu.move(x-self.width(), y)

class ToggleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.isOn = False
        self.setStyleSheet("opacity: 0;")
        self.setGeometry(172, 13, 46, 28)
        # panel
        self.panel = QWidget(self)
        self.panel.setStyleSheet("background-color: #000; border-radius: 4px;")
        self.panel.resize(44, 25)
        # switch
        self.switch = QWidget(self)
        self.switch.setStyleSheet("background-color: white; border-radius: 3px;")
        self.switch.setGeometry(4, 4, 17, 17)
        # detector
        self.detector = QWidget(self)
        self.detector.resize(42, 25)
        self.detector.setStyleSheet("opacity: 0;")
        self.detector.mousePressEvent = self.switch_toggle
        # animation
        #   switch
        self.switch_anim = QPropertyAnimation(self.switch, b"pos")
        self.switch_anim.setDuration(200)
        #   color
        effect = QGraphicsColorizeEffect(self.panel)
        effect.setColor(QColor(145, 145, 145))
        self.panel.setGraphicsEffect(effect)
        self.color_anim = QPropertyAnimation(effect, b"color")

    def switch_toggle(self, event):
        if not self.isOn:
            # change toggle color animation
            self.switch_anim.setEndValue(QPoint(22, 4))
            self.switch_anim.start()
            self.color_anim.setEndValue(QColor(114, 194, 114))
            self.color_anim.start()
            # set is on
            self.isOn = True
        else:
            # change toggle color animation
            self.switch_anim.setEndValue(QPoint(4, 4))
            self.switch_anim.start()
            self.color_anim.setEndValue(QColor(145, 145, 145))
            self.color_anim.start()
            # set is off
            self.isOn = False

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)

class CreateNewButtonWidget(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Create New +", parent)
        # Config
        self.setObjectName("create_new_button")

class AchievementMenuWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # set background transparent
        self.resize(230, 268)
        # Main Menu
        #   Panel
        self.panel = QWidget(self)
        self.panel.resize(self.size())
        self.panel.setObjectName("panel")
        #   Buttons
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(3, 7, 3, 0)
        #       All Achievement Button
        self.all_achievement_button = MenuButtonWidget("All Achievement")
        self.layout.addWidget(self.all_achievement_button)
        #       Create New Button
        self.create_new_button = CreateNewButtonWidget()
        self.create_new_button.clicked.connect(self.sliding_page_in)
        self.layout.addWidget(self.create_new_button)
        self.panel.setLayout(self.layout)
        # Create New Page
        #   Panel
        self.panel_2 = QWidget(self)
        self.panel_2.setObjectName("panel")
        self.panel_2.resize(self.size())
        self.panel_2.move(self.width(), 0)
        #   Sliding Page Animation
        self.sliding_page_anim = QPropertyAnimation(self.panel_2, b"pos")
        self.sliding_page_anim.setEasingCurve(QEasingCurve.Type.OutCurve)
        #   Back Button
        self.back_button = QPushButton(self.panel_2)
        self.back_button.clicked.connect(self.sliding_page_out)
        self.back_button.setObjectName("back_button")
        #   Image Upload Button
        self.image_upload_button = QToolButton(self.panel_2)
        self.image_upload_button.setIcon(QIcon("trophy_icon.png"))
        self.image_upload_button.setIconSize(QSize(60, 60))
        self.image_upload_button.move(10, 50)
        #   Title Entry
        self.title_label = QLabel("Title", self.panel_2)
        self.title_label.move(90, 54)
        self.title_entry = QLineEdit(self.panel_2)
        self.title_entry.move(90, 74)
        #   Summary Entry
        self.summary_label = QLabel("Summary", self.panel_2)
        self.summary_label.move(10, 150)
        self.summary_entry = QLineEdit(self.panel_2)
        self.summary_entry.move(10, 170)

    def sliding_page_in(self):
        self.sliding_page_anim.setDuration(300)
        self.sliding_page_anim.setEndValue(QPoint(0, 0))
        self.sliding_page_anim.start()

    def sliding_page_out(self):
        self.sliding_page_anim.setDuration(100)
        self.sliding_page_anim.setEndValue(QPoint(self.width(), 0))
        self.sliding_page_anim.start()

class MenuButtonWidget(QPushButton):
    def __init__(self, title="", parent=None, has_toggle=False):
        super().__init__(parent)
        # config
        self.setObjectName("menu_button")
        # title
        self.title = QLabel(title, self)
        self.title.setFont(font)
        self.title.move(43, 6)
        self.title.setObjectName("menu_button_title")
        # icon
        self.setIcon(QIcon("trophy_icon.png"))
        self.setIconSize(QSize(28, 28))
        # toggle
        if has_toggle:
            self.toggle = ToggleWidget(self)


main_menu = MainMenuWindow()

# window.show()
tray.activated.connect(show_menu)

app.exec()
