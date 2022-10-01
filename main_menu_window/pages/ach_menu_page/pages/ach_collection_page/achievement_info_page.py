from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QSize, QPoint
from PyQt6.QtGui import QIcon, QPainter
from PyQt6.QtWidgets import QWidget, QToolButton, QLabel, QPlainTextEdit, QPushButton, QStyleOption, QStyle

from main_menu_window.config import *
from main_menu_window.pages.ach_menu_page.pages.ach_collection_page.achievement_collection_button import \
    AchievementCollectionButton


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
        # Element
        # --- Background
        self.background = QWidget(self)
        self.background.setObjectName("panel")
        self.background.resize(self.size())
        # --- Back Button
        self.back_button = QPushButton("< Back", self)
        self.back_button.setObjectName("back_button")
        self.back_button.resize(50, 20)
        self.back_button.move(3, 3)
        self.back_button.clicked.connect(self.hide)
        # --- Delete Button (not implemented)
        self.delete_button = QToolButton(self)
        self.delete_button.setStyleSheet("""
            QToolButton {
                background-color: transparent;
            }
            QToolButton::hover {
                background-color: rgba(255, 255, 255, 50)
            }
        """)
        self.delete_button.setIcon(QIcon("images/trash_bin.png"))
        self.delete_button.setIconSize(QSize(24, 24))
        self.delete_button.resize(30, 30)
        self.delete_button.move(170, 10)
        # --- Edit Button (not implemented)
        self.edit_button = QToolButton(self)
        self.edit_button.resize(30, 30)
        self.edit_button.move(210, 10)
        # --- Icon
        self.icon = QToolButton(self)
        self.icon.setIcon(QIcon("images/trophy_icon.png"))
        self.icon.setObjectName("icon")
        self.icon.setIconSize(QSize(60, 60))
        self.icon.resize(60, 60)
        self.icon.move(10, 50)
        # --- Title
        # ------ label
        self.title_label = QLabel("TITLE", self)
        self.title_label.setStyleSheet("""font-weight: bold;""")
        self.title_label.move(10, 124)
        # ------ text
        self.title_text = QLabel(self)
        self.title_text.move(14, 144)
        # --- Summary
        # ------ label
        self.summary_label = QLabel("SUMMARY", self)
        self.summary_label.setStyleSheet("""font-weight: bold;""")
        self.summary_label.move(10, 174)
        # ------ text
        self.summary_text = QLabel(self)
        self.summary_text.move(14, 194)
        # --- Description
        # ------ label
        self.description_label = QLabel("DESCRIPTION", self)
        self.description_label.setStyleSheet("""font-weight: bold;""")
        self.description_label.move(10, 224)
        # ------ field
        self.description_field = QPlainTextEdit(self)
        self.description_field.setDisabled(True)
        self.description_field.setStyleSheet("""
                    QPlainTextEdit::disabled {
                        background-color: transparent;
                        color: white;
                    }
                """)
        self.description_field.setContentsMargins(0, 0, 0, 0)
        self.description_field.resize(226, 96)
        self.description_field.move(10, 240)

    def setInfo(self, title, summary, description):
        self.title_text.setText(title)
        self.title_text.adjustSize()
        self.summary_text.setText(summary)
        self.summary_text.adjustSize()
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
