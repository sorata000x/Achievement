from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QSize, Qt, QPoint
from PyQt6.QtGui import QIcon, QPainter
from PyQt6.QtWidgets import QWidget, QToolButton, QLabel, QSlider, QPlainTextEdit, QPushButton, QStyleOption, QStyle

from main_menu_window.config import *
from main_menu_window.pages.ach_menu_page.widgets.current_ach_button import CurrentAchievementButton


class CurrentAchievementInfoPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Config
        self.setObjectName("current_achievement_info_page")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # Target Achievement Button
        self.achievement_button = CurrentAchievementButton()    # corresponding achievement button of the info
        # Animation
        self.sliding_page_anim = QPropertyAnimation(self, b"pos")
        self.sliding_page_anim.setEasingCurve(QEasingCurve.Type.OutCurve)
        # Back Button
        self.back_button = QToolButton(self)
        self.back_button.resize(30, 30)
        self.back_button.clicked.connect(self.hide)
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
        self.progress_bar.valueChanged.connect(
            lambda _: self.achievement_button.progress_bar.setValue(self.progress_bar.value()))
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

    def setInfo(self, title, summary, description, achievement_button):
        self.title.setText(title)
        self.title.adjustSize()
        self.summary.setText(summary)
        self.summary.adjustSize()
        self.description_field.setPlainText(description)
        self.achievement_button = achievement_button

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
