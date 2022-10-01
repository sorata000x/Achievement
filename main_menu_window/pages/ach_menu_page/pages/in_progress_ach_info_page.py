from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QSize, Qt, QEvent, pyqtSignal
from PyQt6.QtGui import QIcon, QPainter, QMouseEvent
from PyQt6.QtWidgets import QWidget, QToolButton, QLabel, QSlider, QPushButton, QStyleOption, QStyle, \
    QLineEdit, QTextEdit, QButtonGroup

from main_menu_window.config import *
from ..data.achievement_info import AchievementInfo


class CurrentAchievementInfoPage(QWidget):
    """ Note: Please set info from target achievement button before open. """
    closed = pyqtSignal()

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
        self.delete_button.resize(30, 30)
        self.delete_button.move(170, 10)
        # --- Edit Button (not implemented)
        self.edit_button = QToolButton(self)
        self.edit_button.setStyleSheet("""background: transparent;""")
        self.edit_button.resize(26, 26)
        self.edit_button.setIcon(QIcon("images/edit.png"))
        self.edit_button.setIconSize(QSize(26, 26))
        self.edit_button.move(210, 10)
        # --- Info
        # ------ Icon
        self.icon = QToolButton(self)
        self.icon.setIcon(QIcon("images/trophy_icon.png"))
        self.icon.setObjectName("icon")
        self.icon.setIconSize(QSize(60, 60))
        self.icon.resize(60, 60)
        self.icon.move(10, 50)
        # ------ Title
        # --------- Label
        self.title_label = QLabel("TITLE", self)
        self.title_label.setStyleSheet("""font-weight: bold;""")
        self.title_label.move(10, 124)
        # --------- Entry
        self.title_entry = TitleLineEdit(self)
        self.title_entry.move(14, 144)
        # ------------ add to entry group
        self.entry_group.addEntry(self.title_entry)
        # ------ Summary
        # --------- Label
        self.summary_label = QLabel("SUMMARY", self)
        self.summary_label.setStyleSheet("""font-weight: bold;""")
        self.summary_label.move(10, 174)
        # --------- Entry
        self.summary_entry = SummaryLineEdit(self)
        self.summary_entry.move(14, 194)
        # ------------ add to entry group
        self.entry_group.addEntry(self.summary_entry)
        # ------ Progress
        # --------- Label
        self.progress_label = QLabel("PROGRESS", self)
        self.progress_label.setStyleSheet("""font-weight: bold;""")
        self.progress_label.move(10, 224)
        # --------- Bar
        self.progress_bar = QSlider(Qt.Orientation.Horizontal, self)
        self.progress_bar.setObjectName("info_progress")
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(10)
        self.progress_bar.setFixedWidth(225)
        self.progress_bar.valueChanged.connect(
            lambda: self.achievement_info.setProgress(self.progress_bar.value()))
        self.progress_bar.move(14, 244)
        # ------ Description
        # --------- Label
        self.description_label = QLabel("DESCRIPTION", self)
        self.description_label.setStyleSheet("""font-weight: bold;""")
        self.description_label.move(10, 274)
        # --------- Entry
        self.description_entry = DescriptionTextEdit(self)
        self.description_entry.resize(226, 96)
        self.description_entry.move(14, 294)
        # ------------ add to entry group
        self.entry_group.addEntry(self.description_entry)

    def hide(self) -> None:
        super().hide()
        self.closed.emit()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.entry_group.disableAll()

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
