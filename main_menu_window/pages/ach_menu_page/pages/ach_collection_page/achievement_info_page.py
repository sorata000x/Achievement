from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QSize, Qt, QPoint
from PyQt6.QtGui import QIcon, QPainter
from PyQt6.QtWidgets import QWidget, QToolButton, QLabel, QSlider, QPlainTextEdit, QPushButton, QStyleOption, QStyle

from main_menu_window.config import *
from main_menu_window.pages.ach_menu_page.pages.ach_collection_page.achievement_collection_button import \
    AchievementCollectionButton
from main_menu_window.pages.ach_menu_page.widgets.current_ach_button import CurrentAchievementButton


class AchievementInfoPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Config
        self.setObjectName("current_achievement_info_page")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # Target Achievement Button
        self.achievement_button = AchievementCollectionButton()    # corresponding achievement button of the info
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
        # Icon
        self.icon = QToolButton(self)
        self.icon.setIcon(QIcon("images/trophy_icon.png"))
        self.icon.setObjectName("icon")
        self.icon.setIconSize(QSize(50, 50))
        self.icon.resize(50, 50)
        self.icon.move(int(self.width()/2-self.icon.width()/2-10), 50)
        # Title
        self.title = QLabel(self)
        self.title.setStyleSheet("color: black; font-size: 22pt;")
        self.title.move(15, 110)
        # Summary
        self.summary = QLabel(self)
        self.summary.setStyleSheet("color: black; font-size: 16pt;")
        self.summary.move(15, 140)
        # Description
        self.description_label = QLabel("DESCRIPTION", self)
        self.description_label.move(15, 170)
        self.description_field = QPlainTextEdit(self)
        self.description_field.setDisabled(True)
        self.description_field.setStyleSheet("""
            QPlainTextEdit::disabled {
                background-color: gray;
                color: white;
            }
        """)
        self.description_field.resize(226, 96)
        self.description_field.move(15, 190)

    def setInfo(self, title, summary, description):
        self.title.setText(title)
        self.title.adjustSize()
        self.summary.setText(summary)
        self.summary.adjustSize()
        self.description_field.setPlainText(description)
        #self.achievement_button = achievement_button

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
