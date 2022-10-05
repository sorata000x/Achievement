from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QSize, QPoint, pyqtSignal
from PyQt6.QtGui import QIcon, QPainter
from PyQt6.QtWidgets import QWidget, QToolButton, QLabel, QPlainTextEdit, QPushButton, QStyleOption, QStyle, QMessageBox

from main_menu_window.config import *
from main_menu_window.pages.ach_menu_page.pages.ach_collection_page.achievement_collection_button import \
    AchievementCollectionButton
from main_menu_window.pages.ach_menu_page.pages.widgets.delete_confirm_box import DeleteConfirmBox
from ...data.achievement_info import AchievementInfo


class AchievementInfoPage(QWidget):
    deleted = pyqtSignal()      # deleted the corresponding achievement, not the page.

    def __init__(self, parent=None):
        super().__init__(parent)
        # Config
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
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
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #437ccc;
            }
            QPushButton::hover {
                color: #7aa6e6;
            }
        """)
        self.back_button.resize(50, 20)
        self.back_button.move(3, 3)
        self.back_button.clicked.connect(self.hide)
        # ------ Page title
        self.page_title = QLabel(self)
        self.page_title.setStyleSheet("""color: #adb1b8; font-size: 14pt;""")
        self.page_title.setText("Achievement Info")
        self.page_title.move(62, 6)
        # --- Delete Button
        self.delete_button = QToolButton(self)
        self.delete_button.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border-radius: 1px;
            }
            QToolButton::hover {
                background-color: rgba(255, 255, 255, 50)
            }
        """)
        self.delete_button.setIcon(QIcon("images/trash_bin.png"))
        self.delete_button.setIconSize(QSize(24, 24))
        self.delete_button.resize(30, 30)
        self.delete_button.move(200, 10)
        # --- Icon
        self.icon = QToolButton(self)
        self.icon.setIcon(QIcon("images/trophy.png"))
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
        # --- Deletion Confirm Message Box
        self.deletion_confirm_box = DeleteConfirmBox(self)
        self.deletion_confirm_box.move(
            int(self.width()/2-self.deletion_confirm_box.width()/2),
            int(self.height()/2-self.deletion_confirm_box.height()/2)
        )
        self.deletion_confirm_box.hide()
        self.delete_button.clicked.connect(self.deletion_confirm_box.show)
        self.deletion_confirm_box.delete_button.clicked.connect(self.deleted.emit)

    def setInfo(self, achievement_info):
        # Set title
        self.title_text.setText(achievement_info.title())
        self.title_text.adjustSize()
        # Set summary
        self.summary_text.setText(achievement_info.summary())
        self.summary_text.adjustSize()
        # Set description
        self.description_field.setPlainText(achievement_info.description())

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)

    def sliding_page_in(self):
        """ NOT IN USE """
        self.sliding_page_anim.setDuration(300)
        self.sliding_page_anim.setEndValue(QPoint(0, 0))
        self.sliding_page_anim.start()

    def sliding_page_out(self):
        """ NOT IN USE """
        self.sliding_page_anim.setDuration(100)
        self.sliding_page_anim.setEndValue(QPoint(self.width(), 0))
        self.sliding_page_anim.start()
