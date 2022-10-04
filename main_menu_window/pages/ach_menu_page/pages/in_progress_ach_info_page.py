from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QSize, Qt, QEvent, pyqtSignal
from PyQt6.QtGui import QIcon, QPainter, QMouseEvent
from PyQt6.QtWidgets import QWidget, QToolButton, QLabel, QSlider, QPushButton, QStyleOption, QStyle, \
    QLineEdit, QTextEdit, QButtonGroup

from main_menu_window.config import *
from .widgets.delete_confirm_box import DeleteConfirmBox
from ..data.achievement_info import AchievementInfo


class InProgressAchievementInfoPage(QWidget):
    """ Note: Please set info from target achievement button before open. """
    closed = pyqtSignal()       # page closed
    deleted = pyqtSignal()      # deleted the corresponding achievement, not the page.

    def __init__(self, parent=None):
        super().__init__(parent)
        # Page Config
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # Property
        # --- Target Achievement Info
        self.achievement_info = AchievementInfo()  # corresponding achievement button of the info
        # --- Group of LineEdit or TextEdit of info
        self.entry_group = EntryGroup()
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
                border-radius: 1px;
            }
            QToolButton::hover {
                background-color: rgba(255, 255, 255, 50)
            }
        """)
        self.delete_button.setIcon(QIcon("images/trash_bin.png"))
        self.delete_button.setIconSize(QSize(20, 20))
        self.delete_button.resize(30, 30)
        self.delete_button.move(200, 10)
        # --- Info
        self.page_title = QLabel(self)
        self.page_title.setStyleSheet("""font-size: 14pt;""")
        self.page_title.setText("Achievement Info")
        self.page_title.move(62, 6)
        # ------ Icon
        self.icon = QToolButton(self)
        self.icon.setStyleSheet("""background-color: black;""")
        self.icon.setIcon(QIcon("images/trophy.png"))
        self.icon.setObjectName("icon")
        self.icon.setIconSize(QSize(60, 60))
        self.icon.resize(60, 60)
        self.icon.move(10, 42)
        # ------ Title
        # --------- Label
        self.title_label = QLabel("TITLE", self)
        self.title_label.setStyleSheet("""font-weight: bold;""")
        self.title_label.move(11, 116)
        # --------- Entry
        self.title_entry = TitleLineEdit(self)
        self.title_entry.move(14, 136)
        # ------------ add to entry group
        self.entry_group.addEntry(self.title_entry)
        # ------ Summary
        # --------- Label
        self.summary_label = QLabel("SUMMARY", self)
        self.summary_label.setStyleSheet("""font-weight: bold;""")
        self.summary_label.move(11, 166)
        # --------- Entry
        self.summary_entry = SummaryLineEdit(self)
        self.summary_entry.move(14, 186)
        # ------------ add to entry group
        self.entry_group.addEntry(self.summary_entry)
        # ------ Progress
        # --------- Label
        self.progress_label = QLabel("PROGRESS", self)
        self.progress_label.setStyleSheet("""font-weight: bold;""")
        self.progress_label.move(11, 216)
        # --------- Bar
        self.progress_bar = QSlider(Qt.Orientation.Horizontal, self)
        self.progress_bar.setStyleSheet("""
            QSlider::groove:horizontal {
                background-color: black;
                height: 18px;
            }
            QSlider::handle:horizontal {
                background-color: #9c9c9c;
                width: 3px;
                border-radius: 1px;
                margin: -2px 0px;
            }
            QSlider::sub-page:horizontal {
                background-color: #344f6e;
            }
        """)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(10)
        self.progress_bar.setFixedWidth(self.width()-40)
        self.progress_bar.valueChanged.connect(
            lambda: self.achievement_info.setProgress(self.progress_bar.value()))
        self.progress_bar.move(20, 236)
        # ------ Description
        # --------- Label
        self.description_label = QLabel("DESCRIPTION", self)
        self.description_label.setStyleSheet("""font-weight: bold;""")
        self.description_label.move(11, 266)
        # --------- Entry
        self.description_entry = DescriptionTextEdit(self)
        self.description_entry.resize(226, 96)
        self.description_entry.move(14, 286)
        # ------------ add to entry group
        self.entry_group.addEntry(self.description_entry)
        # --- Deletion Confirm Message Box
        self.deletion_confirm_box = DeleteConfirmBox(self)
        self.deletion_confirm_box.move(
            int(self.width() / 2 - self.deletion_confirm_box.width() / 2),
            int(self.height() / 2 - self.deletion_confirm_box.height() / 2)
        )
        self.deletion_confirm_box.hide()
        self.delete_button.clicked.connect(self.deletion_confirm_box.show)
        self.deletion_confirm_box.delete_button.clicked.connect(self.deleted.emit)

    # Page Function

    def setInfo(self, achievement_info):
        self.achievement_info = achievement_info
        # title entry
        self.title_entry.setText(achievement_info.title())
        self.title_entry.adjustSize()
        self.title_entry.setTarget(achievement_info)
        # summary entry
        self.summary_entry.setText(achievement_info.summary())
        self.summary_entry.adjustSize()
        self.summary_entry.setTarget(achievement_info)
        # description entry
        self.description_entry.setPlainText(achievement_info.description())
        self.description_entry.setTarget(achievement_info)
        # progress bar
        self.progress_bar.setValue(achievement_info.progress())

    # Events

    def hide(self) -> None:
        super().hide()
        self.closed.emit()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.entry_group.disableAll()

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)

class TitleLineEdit(QLineEdit):
    clicked = pyqtSignal()
    double_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Property
        self.target = AchievementInfo()
        # Config
        self.setReadOnly(True)

    def setTarget(self, target):
        self.target = target

    def setReadOnly(self, a0: bool) -> None:
        super().setReadOnly(a0)
        if a0:
            self.target.setTitle(self.text())

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        super().mousePressEvent(a0)
        self.clicked.emit()

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        super().mouseDoubleClickEvent(a0)
        self.double_clicked.emit()

class SummaryLineEdit(QLineEdit):
    clicked = pyqtSignal()
    double_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Property
        self.target = AchievementInfo()
        # Config
        self.setReadOnly(True)

    def setTarget(self, target):
        self.target = target

    def setReadOnly(self, a0: bool) -> None:
        super().setReadOnly(a0)
        if a0:
            self.target.setSummary(self.text())

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        super().mousePressEvent(a0)
        self.clicked.emit()

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        super().mouseDoubleClickEvent(a0)
        self.double_clicked.emit()

class DescriptionTextEdit(QTextEdit):
    clicked = pyqtSignal()
    double_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Property
        self.target = AchievementInfo()
        # Config
        self.setReadOnly(True)

    def setTarget(self, target):
        self.target = target

    def setReadOnly(self, a0: bool) -> None:
        super().setReadOnly(a0)
        if a0:
            self.viewport().setCursor(Qt.CursorShape.ArrowCursor)
            self.setStyleSheet("""
                background-color: transparent; 
                color: white; 
                border: none; 
                border-radius: 2px;
            """)
            self.target.setDescription(self.toPlainText())
        else:
            self.viewport().setCursor(Qt.CursorShape.IBeamCursor)
            self.setStyleSheet("""
                background-color: #484b4f; 
                color: white; 
                border: none; 
                border-radius: 2px;
            """)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        super().mousePressEvent(a0)
        self.clicked.emit()

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        super().mouseDoubleClickEvent(a0)
        self.double_clicked.emit()


class EntryGroup:
    def __init__(self):
        self.entry_group = []

    def addEntry(self, entry):
        entry.clicked.connect(lambda: self.disableOther(entry))
        entry.double_clicked.connect(lambda: self.disableOther(entry))
        entry.double_clicked.connect(lambda: entry.setReadOnly(False))
        self.entry_group.append(entry)

    def disableOther(self, source):
        for edit in self.entry_group:
            if edit != source:
                edit.setReadOnly(True)

    def disableAll(self):
        for edit in self.entry_group:
            edit.setReadOnly(True)
