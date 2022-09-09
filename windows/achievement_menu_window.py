from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QSize
from PyQt6.QtGui import QIcon, QPainter, QFontMetricsF
from PyQt6.QtWidgets import QWidget, QPushButton, QScrollArea, QVBoxLayout, QToolButton, QLabel, QSlider, \
    QPlainTextEdit, QStyleOption, QStyle, QProgressBar, QLineEdit
from .config import *
from widgets.menu_button import MenuButtonWidget
from widgets.create_new_button import CreateNewButtonWidget

class AchievementMenuWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Window Config
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # set background transparent
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # Main Menu
        self.main_menu = self.MainMenu(self)
        # Create-New Page
        self.create_new_page = self.CreateNewPage(self)
        self.main_menu.create_new_button.clicked.connect(self.create_new_page.sliding_page_in)
        self.create_new_page.cancel_button.clicked.connect(self.create_new_page.sliding_page_out)
        self.create_new_page.ok_button.clicked.connect(self.create_new_achievement)

# TEST
        last_index = self.main_menu.cab_layout.indexOf(self.main_menu.create_new_button)
        achievement = self.CurrentAchievementButton("Title", "A bit longer summary", "Some description")
        self.main_menu.cab_layout.insertWidget(last_index, achievement)

        # --------- Current Achievement Info Page
        self.current_achievement_info_page = self.CurrentAchievementInfoPage(self)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key.Key_Return:
            self.create_new_achievement()

    def sliding_page_in(self, page):
        sliding_page_anim = QPropertyAnimation(page, b"pos")
        sliding_page_anim.setEasingCurve(QEasingCurve.Type.OutCurve)
        sliding_page_anim.setDuration(300)
        sliding_page_anim.setEndValue(QPoint(0, 0))
        sliding_page_anim.start()

    def sliding_page_out(self, page):
        sliding_page_anim = QPropertyAnimation(page, b"pos")
        sliding_page_anim.setEasingCurve(QEasingCurve.Type.OutCurve)
        sliding_page_anim.setDuration(100)
        sliding_page_anim.setEndValue(QPoint(self.width(), 0))
        sliding_page_anim.start()

    def create_new_achievement(self):
        new_achievement_button = self.CurrentAchievementButton(
            self.create_new_page.title_entry.text(),
            self.create_new_page.summary_entry.text(),
            self.create_new_page.description_entry.toPlainText()
        )

        def openCurrentAchievementInfoPage():
            self.current_achievement_info_page.setInfo(new_achievement_button)
            self.current_achievement_info_page.sliding_page_in()

        new_achievement_button.clicked.connect(openCurrentAchievementInfoPage)
        self.main_menu.current_achievement_buttons.append(new_achievement_button)

        last_index = self.main_menu.cab_layout.indexOf(self.main_menu.create_new_button)
        self.main_menu.cab_layout.insertWidget(last_index, new_achievement_button)
        self.create_new_page.sliding_page_out()

    class MainMenu(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
            # --- Background
            self.background = QWidget(self)
            self.background.resize(self.size())
            self.background.setObjectName("panel")
            # ------ Back Button
            self.back_button = QPushButton("< Tool menu", self)
            #self.back_button.clicked.connect()
            # ------ All Achievement Button
            self.all_achievement_button = MenuButtonWidget("Collection", self)
            self.all_achievement_button.setFixedWidth(226)
            self.all_achievement_button.setFixedHeight(50)
            self.all_achievement_button.move(3, 33)
            # --- Achievements Buttons
            # ------ Widget to contain scroll area for resizing
            self.ab_scroll_area_container = QWidget(self)
            self.ab_scroll_area_container.resize(self.width(), 270)
            self.ab_scroll_area_container.move(0, 83)
            # ------ Scroll Area, to contain buttons
            self.ab_scroll_area = QScrollArea(self.ab_scroll_area_container)
            self.ab_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            self.ab_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.ab_scroll_area.setWidgetResizable(True)
            self.ab_scroll_area.resize(self.width()-5, 264)
            self.ab_scroll_area.move(3, 3)
            self.ab_scroll_area.setContentsMargins(0, 0, 0, 0)
            # --------- Widget to contain created achievement buttons layout
            self.cab_widget = QWidget()
            self.cab_widget.setFixedWidth(226)
            self.cab_widget.setObjectName("panel")
            self.ab_scroll_area.setWidget(self.cab_widget)
            # --------- Layout
            self.cab_layout = QVBoxLayout()
            self.cab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.cab_layout.setContentsMargins(0, 0, 0, 0)
            self.cab_layout.setSpacing(15)
            self.cab_widget.setLayout(self.cab_layout)
            # --------- Create New Button: always at bottom
            self.create_new_button = CreateNewButtonWidget()
            self.create_new_button.setFixedWidth(226)
            self.cab_layout.addWidget(self.create_new_button)
            # --------- Current Achievement Buttons
            self.current_achievement_buttons = []

    class CreateNewPage(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            # Config
            self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
            self.move(self.width(), 0)
            # Animation
            self.sliding_page_anim = QPropertyAnimation(self, b"pos")
            self.sliding_page_anim.setEasingCurve(QEasingCurve.Type.OutCurve)
            # Background
            self.background = QWidget(self)
            self.background.setObjectName("panel")
            self.background.resize(self.size())
            # Image Upload Button
            self.image_upload_button = QToolButton(self.background)
            self.image_upload_button.setIcon(QIcon("images/trophy_icon.png"))
            self.image_upload_button.setIconSize(QSize(60, 60))
            self.image_upload_button.move(10, 10)
            # Title Entry
            self.title_label = QLabel("TITLE", self.background)
            self.title_label.move(92, 38)
            self.title_entry = QLineEdit(self.background)
            self.title_entry.move(92, 56)
            self.title_entry.resize(144, 24)
            self.title_entry.setStyleSheet("""
                        background-color: #2b2b2b; 
                        border: 0; border-radius: 2px; 
                        padding: 2px; 
                        color: white;
                        """)
            # Summary Entry
            self.summary_label = QLabel("SUMMARY", self.background)
            self.summary_label.move(10, 90)
            self.summary_entry = QLineEdit(self.background)
            self.summary_entry.move(10, 108)
            self.summary_entry.setStyleSheet("""
                        background-color: #2b2b2b; 
                        border: 0; border-radius: 2px; 
                        padding: 2px; 
                        color: white;
                        height: 20px;
                        width: 222px;
                        """)
            # Description Entry
            self.description_label = QLabel("DESCRIPTION", self.background)
            self.description_label.move(10, 140)
            self.description_entry = QPlainTextEdit(self.background)
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
            # Cancel Button
            self.cancel_button = QPushButton("Cancel", self.background)
            self.cancel_button.resize(66, 24)
            self.cancel_button.move(94, 264)
            self.cancel_button.setStyleSheet("""
                        background-color: #636363;
                        border-radius: 2px;
                        color: white;
                    """)
            # OK Button
            self.ok_button = QPushButton("OK", self.background)
            self.ok_button.resize(66, 24)
            self.ok_button.move(170, 264)
            self.ok_button.setStyleSheet("""
                        background-color: #198cff;
                        border-radius: 2px;
                        color: white;
                    """)

        def sliding_page_in(self):
            self.sliding_page_anim.setDuration(300)
            self.sliding_page_anim.setEndValue(QPoint(0, 0))
            self.sliding_page_anim.start()

        def sliding_page_out(self):
            self.sliding_page_anim.setDuration(100)
            self.sliding_page_anim.setEndValue(QPoint(self.width(), 0))
            self.sliding_page_anim.start()

    class CurrentAchievementInfoPage(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            # Config
            self.setObjectName("current_achievement_info_page")
            self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
            self.move(self.width(), 0)
            # Animation
            self.sliding_page_anim = QPropertyAnimation(self, b"pos")
            self.sliding_page_anim.setEasingCurve(QEasingCurve.Type.OutCurve)
            # Back Button
            self.back_button = QToolButton(self)
            self.back_button.resize(30, 30)
            self.back_button.clicked.connect(self.sliding_page_out)
            # Delete Button
            self.delete_button = QToolButton(self)
            self.delete_button.resize(30, 30)
            self.delete_button.move(170, 10)
            # Edit Button
            self.edit_button = QToolButton(self)
            self.edit_button.resize(30, 30)
            self.edit_button.move(210, 10)
            # Title
            self.title = QLabel(self)
            self.title.setStyleSheet("color: black; font-size: 18pt;")
            self.title.move(78, 53)
            # Icon
            self.icon = QToolButton(self)
            self.icon.setIcon(QIcon("images/trophy_icon.png"))
            self.icon.setObjectName("icon")
            self.icon.setIconSize(QSize(50, 50))
            self.icon.resize(50, 50)
            self.icon.move(16, 50)
            # Summary
            self.summary = QLabel(self)
            self.summary.setStyleSheet("color: black; font-size: 14pt;")
            self.summary.move(78, 78)
            # Progress
            self.progress_label = QLabel("PROGRESS", self)
            self.progress_label.move(15, 112)
            self.progress_bar = QSlider(Qt.Orientation.Horizontal, self)
            self.progress_bar.setObjectName("info_progress")
            self.progress_bar.setMinimum(0)
            self.progress_bar.setMaximum(10)
            self.progress_bar.setFixedWidth(225)
            self.progress_bar.move(15, 128)
            # Description
            self.description_label = QLabel("DESCRIPTION", self)
            self.description_label.move(15, 160)
            self.description_field = QPlainTextEdit(self)
            self.description_field.setDisabled(True)
            self.description_field.setStyleSheet("""
                QPlainTextEdit::disabled {
                    background-color: gray;
                    color: white;
                }
            """)
            self.description_field.resize(226, 96)
            self.description_field.move(15, 178)
            # Complete Button
            self.complete_button = QPushButton("COMPLETE", self)
            self.complete_button.resize(160, 50)
            self.complete_button.setStyleSheet("""
                background-color: gray;
                color: white;
                font-size: 16pt;
            """)
            self.complete_button.move(46, 287)

        def setInfo(self, achievement):
            self.title.setText(achievement.title.text())
            self.title.adjustSize()
            self.summary.setText(achievement.summary.text())
            self.summary.adjustSize()
            self.description_field.setPlainText(achievement.description)

        def paintEvent(self, pe):
            o = QStyleOption()
            o.initFrom(self)
            p = QPainter(self)
            self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)

        def sliding_page_in(self):
            self.sliding_page_anim.setDuration(300)
            self.sliding_page_anim.setEndValue(QPoint(0, 0))
            self.sliding_page_anim.start()

        def sliding_page_out(self):
            self.sliding_page_anim.setDuration(100)
            self.sliding_page_anim.setEndValue(QPoint(self.width(), 0))
            self.sliding_page_anim.start()

    class CurrentAchievementButton(QPushButton):
        def __init__(self, title="", summary="", description="", parent=None):
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
            self.icon.setIcon(QIcon("images/trophy_icon.png"))
            self.icon.setObjectName("icon")
            self.icon.setIconSize(QSize(30, 30))
            self.icon.resize(36, 36)
            self.icon.move(6, 7)
            # Summary
            self.summary = QLabel(summary, self)
            self.summary.setObjectName("current_achievement_button_summary")
            self.summary.move(48, 28)
            # Description
            self.description = description

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
                if p_int > self.maximum() * (99 / 100):
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

