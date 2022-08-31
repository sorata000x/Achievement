"""
    Objective: For RPGOverlay; To have system tray with window right below it.
    Current:
        - Icon tray & menu with utilities buttons and achievement menu
    To Do:

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

# Create the App
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

# Set App Font
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

# Create the Tray
tray = QSystemTrayIcon()
tray.setIcon(QIcon("icon.jpg"))
tray.setVisible(True)

def toggle_menu():
    """
    Show menu window when it is hidden, otherwise hide the window.
    :return:
    """
    if main_menu.isHidden():
        main_menu.move(tray.geometry().bottomLeft().x(), tray.geometry().bottomLeft().y()+5)
        main_menu.show()
    else:
        main_menu.hide()
    return


tray.activated.connect(toggle_menu)

class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Window config
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # set background transparent
        self.width = 230
        self.height = 298
        self.resize(self.width, self.height)
        # Panel
        self.panel = QWidget(self)
        self.panel.resize(self.size())
        self.panel.setObjectName("panel")
        # Sub windows
        self.achievement_menu = AchievementMenuWindow()
        # Buttons
        self.buttons = QWidget(self.panel)
        self.buttons.resize(230, 268)
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
        #   DEBUG
        self.menu_buttons["quit"].clicked.connect(app.quit)
        self.buttons.setLayout(self.layout)
        #   Tools
        self.setting_button = QToolButton(self.panel)
        self.setting_button.move(4, 268)
        self.user_button = QToolButton(self.panel)
        self.user_button.move(200, 268)

    def move(self, x, y):
        """ Move sub-windows as well."""
        super().move(x, y)
        self.achievement_menu.move(x-self.achievement_menu.width()-2, y)

class ToggleWidget(QWidget):
    """ Animated toggle switch widget. """
    def __init__(self, parent=None):
        super().__init__(parent)
        # Config
        self.isOn = False
        self.setStyleSheet("opacity: 0;")
        self.setGeometry(172, 13, 46, 28)
        # Panel
        self.panel = QWidget(self)
        self.panel.setStyleSheet("background-color: #000; border-radius: 4px;")
        self.panel.resize(44, 25)
        # Switch
        self.switch = QWidget(self)
        self.switch.setStyleSheet("background-color: white; border-radius: 3px;")
        self.switch.setGeometry(4, 4, 17, 17)
        # Detector
        self.detector = QWidget(self)
        self.detector.resize(42, 25)
        self.detector.setStyleSheet("opacity: 0;")
        self.detector.mousePressEvent = self.switch_toggle
        # Animation
        #   Switch Pos Anim
        self.switch_anim = QPropertyAnimation(self.switch, b"pos")
        self.switch_anim.setDuration(200)
        #   Color Anim
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
    """ Button widget to suggest creating new widget. """
    def __init__(self, parent=None):
        super().__init__("Create New +", parent)
        # Config
        self.setObjectName("create_new_button")

class AchievementMenuWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Config
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # set background transparent
        self.resize(250, 298)
        # Main Menu
        # -- Panel
        self.panel = QWidget(self)
        self.panel.resize(self.size())
        self.panel.setObjectName("panel")
        # -- Buttons
        self.stack_layout = QStackedLayout()
        # ---- Widget to contain scroll area for resizing
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.resize(247, 269)
        # ---- Scroll Area, to contain buttons
        self.scroll_area = QScrollArea(self.scroll_area_widget)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.resize(244, 266)
        self.scroll_area.move(3, 3)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        # ---- All Achievement Button, flot on the scroll area
        self.all_achievement_button = MenuButtonWidget("All Achievement", self.scroll_area)
        self.all_achievement_button.setFixedWidth(226)
        self.all_achievement_button.setFixedHeight(50)
        # ---- Create New Button
        # ------ Background Widget
        self.create_new_button_background = QWidget(self.scroll_area)
        self.create_new_button_background.setObjectName("white-background")
        self.create_new_button_background.setFixedWidth(226)
        self.create_new_button_background.setFixedHeight(54)
        self.create_new_button_background.move(0, self.scroll_area.height()-54)
        # ------ Button
        self.create_new_button = CreateNewButtonWidget(self.create_new_button_background)
        self.create_new_button.setFixedWidth(226)
        self.create_new_button.clicked.connect(self.sliding_page_in)
        # ---- Created Achievement Buttons
        # ------ Widget to contain created achievement buttons
        self.created_achievement_buttons_widget = QWidget()
        self.created_achievement_buttons_widget.setFixedWidth(226)
        self.created_achievement_buttons_widget.setObjectName("panel")
        self.scroll_area.setWidget(self.created_achievement_buttons_widget)
        # ------ Layout
        self.created_achievement_buttons_layout = QVBoxLayout()
        self.created_achievement_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.created_achievement_buttons_layout.setContentsMargins(0, 53, 0, 4)
        self.created_achievement_buttons_layout.setSpacing(3)
        self.created_achievement_buttons_widget.setLayout(self.created_achievement_buttons_layout)
        # ------ TESTING
        self.buffer_buttons = [
            MenuButtonWidget("Achievement 1"),
            MenuButtonWidget("Achievement 2"),
            MenuButtonWidget("Achievement 3"),
            MenuButtonWidget("Achievement 4"),
            MenuButtonWidget("Achievement 5"),
        ]
        for b in self.buffer_buttons:
            self.created_achievement_buttons_layout.addWidget(b)

        self.stack_layout.addWidget(self.scroll_area_widget)
        self.panel.setLayout(self.stack_layout)

        # Create-New Page
        # -- Panel
        self.panel_2 = QWidget(self)
        self.panel_2.setObjectName("panel")
        self.panel_2.resize(self.size())
        self.panel_2.move(self.width(), 0)
        # -- Sliding Page Animation
        self.sliding_page_anim = QPropertyAnimation(self.panel_2, b"pos")
        self.sliding_page_anim.setEasingCurve(QEasingCurve.Type.OutCurve)
        # -- Back Button
        self.back_button = QPushButton(self.panel_2)
        self.back_button.clicked.connect(self.sliding_page_out)
        self.back_button.setObjectName("back_button")
        # -- Image Upload Button
        self.image_upload_button = QToolButton(self.panel_2)
        self.image_upload_button.setIcon(QIcon("trophy_icon.png"))
        self.image_upload_button.setIconSize(QSize(60, 60))
        self.image_upload_button.move(10, 50)
        # -- Title Entry
        self.title_label = QLabel("Title", self.panel_2)
        self.title_label.move(92, 64)
        self.title_entry = QLineEdit(self.panel_2)
        self.title_entry.move(92, 82)
        # -- Summary Entry
        self.summary_label = QLabel("Summary", self.panel_2)
        self.summary_label.move(14, 130)
        self.summary_entry = QLineEdit(self.panel_2)
        self.summary_entry.resize(222, 20)
        self.summary_entry.move(14, 150)
        # -- Description Entry
        self.description_label = QLabel("Description", self.panel_2)
        self.description_label.move(14, 180)
        self.description_entry = QLineEdit(self.panel_2)
        self.description_entry.resize(222, 50)
        self.description_entry.move(14, 200)
        # -- OK Button
        self.ok_button = QPushButton("OK", self.panel_2)
        self.ok_button.move(100, 260)
        # -- Cancel Button
        self.cancel_button = QPushButton("Cancel", self.panel_2)
        self.cancel_button.move(170, 260)

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


app.exec()
