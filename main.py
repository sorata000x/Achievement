"""
    Objective: For RPGOverlay; To have system tray with window right below it.
    Current:
        - Icon tray & menu with utilities buttons and achievement menu
    To Do:
        - Button hover effect
"""

import sys
import os
from PyQt6.QtCore import Qt, QSize, QDir, QPropertyAnimation, QPoint, QEasingCurve, pyqtSignal
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
        # Property
        #self.is_create_new_page_shown = False
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
        self.created_achievement_buttons_layout.setContentsMargins(0, 57, 0, 65)
        self.created_achievement_buttons_layout.setSpacing(15)
        self.created_achievement_buttons_widget.setLayout(self.created_achievement_buttons_layout)

        self.stack_layout.addWidget(self.scroll_area_widget)
        self.panel.setLayout(self.stack_layout)

        self.current_achievement_buttons = [

        ]

        """
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

        self.test_button = MenuButtonWidget("Achievement Test")
        """


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
        #self.back_button = QPushButton(self.panel_2)
        #self.back_button.clicked.connect(self.sliding_page_out)
        #self.back_button.setObjectName("back_button")
        # -- Image Upload Button
        self.image_upload_button = QToolButton(self.panel_2)
        self.image_upload_button.setIcon(QIcon("trophy_icon.png"))
        self.image_upload_button.setIconSize(QSize(60, 60))
        self.image_upload_button.move(10, 10)
        # -- Title Entry
        self.title_label = QLabel("TITLE", self.panel_2)
        self.title_label.move(92, 38)
        self.title_entry = QLineEdit(self.panel_2)
        self.title_entry.move(92, 56)
        self.title_entry.resize(144, 24)
        self.title_entry.setStyleSheet("""
            background-color: #2b2b2b; 
            border: 0; border-radius: 2px; 
            padding: 2px; 
            color: white;
            """)
        # -- Summary Entry
        self.summary_label = QLabel("SUMMARY", self.panel_2)
        self.summary_label.move(10, 90)
        self.summary_entry = QLineEdit(self.panel_2)
        self.summary_entry.move(10, 108)
        self.summary_entry.setStyleSheet("""
            background-color: #2b2b2b; 
            border: 0; border-radius: 2px; 
            padding: 2px; 
            color: white;
            height: 20px;
            width: 222px;
            """)
        # -- Description Entry
        self.description_label = QLabel("DESCRIPTION", self.panel_2)
        self.description_label.move(10, 140)
        self.description_entry = QPlainTextEdit(self.panel_2)
        self.description_entry.move(10, 158)
        self.description_entry.resize(226, 96)
        self.description_entry.setStyleSheet("""
            background-color: #2b2b2b; 
            border: 0; border-radius: 2px; 
            padding: 2px; 
            color: white;
            """)
        self.description_entry.setTabStopDistance(
            QFontMetricsF(self.description_entry.font()).horizontalAdvance(' ') * 4)
        # -- Cancel Button
        self.cancel_button = QPushButton("Cancel", self.panel_2)
        self.cancel_button.resize(66, 24)
        self.cancel_button.move(94, 264)
        self.cancel_button.clicked.connect(self.sliding_page_out)
        self.cancel_button.setStyleSheet("""
            background-color: #636363;
            border-radius: 2px;
            color: white;
        """)
        # -- OK Button
        self.ok_button = QPushButton("OK", self.panel_2)
        self.ok_button.resize(66, 24)
        self.ok_button.move(170, 264)
        self.ok_button.clicked.connect(self.create_new_achievement)
        self.ok_button.setStyleSheet("""
            background-color: #198cff;
            border-radius: 2px;
            color: white;
        """)

        # TEST
        #self.current_achievement_buttons.append(self.CurrentAchievementButton("Title", "Summary"))
        self.created_achievement_buttons_layout.addWidget(self.CurrentAchievementButton("Title", "A bit longer summary"))

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        #self.keyPressed.emit(event.key())
        if event.key() == Qt.Key.Key_Return:
            self.create_new_achievement()

    def sliding_page_in(self):
        self.sliding_page_anim.setDuration(300)
        self.sliding_page_anim.setEndValue(QPoint(0, 0))
        self.sliding_page_anim.start()
        #self.is_create_new_page_shown = True

    def sliding_page_out(self):
        self.sliding_page_anim.setDuration(100)
        self.sliding_page_anim.setEndValue(QPoint(self.width(), 0))
        self.sliding_page_anim.start()

    def create_new_achievement(self):
        new_achievement_button = self.CurrentAchievementButton(self.title_entry.text(), self.summary_entry.text())
        self.current_achievement_buttons.append(new_achievement_button)
        self.created_achievement_buttons_layout.addWidget(new_achievement_button)
        self.sliding_page_out()

    class CurrentAchievementButton(QPushButton):
        def __init__(self, title, summary, parent=None):
            super().__init__(parent)
            # Config
            self.setObjectName("current_achievement_button")
            # Progress
            self.progress_bar = self.ProgressBar(self)
            self.progress_bar.setValue(100)
            # Title
            self.title = QLabel(title, self)
            self.title.setObjectName("current_achievement_button_title")
            self.title.move(48, 6)
            # Icon
            self.icon = QToolButton(self)
            self.icon.setIcon(QIcon("trophy_icon.png"))
            self.icon.setObjectName("icon")
            self.icon.setIconSize(QSize(30, 30))
            self.icon.resize(36, 36)
            self.icon.move(6, 7)
            # Summary
            self.summary = QLabel(summary, self)
            self.summary.setObjectName("current_achievement_button_summary")
            self.summary.move(48, 28)

        class ProgressBar(QProgressBar):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setObjectName("progress")
                self.setFormat('')
                self.move(0, 0)
                self.setMinimum(0)
                self.setMaximum(100)

            def setValue(self, p_int):
                super().setValue(p_int)
                if p_int > self.maximum() * (99/100):
                    self.setStyleSheet("""
                        #progress::chunk {
                            background-color: blue;
                            border-radius: 5px;
                        }""")
                else:
                    self.setStyleSheet("""
                        #progress::chunk {
                            background-color: blue;
                            border-top-left-radius: 5px;
                            border-bottom-left-radius: 5px;
                        }""")


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
