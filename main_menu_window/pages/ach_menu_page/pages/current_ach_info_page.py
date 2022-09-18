from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QSize, Qt, QEvent
from PyQt6.QtGui import QIcon, QPainter
from PyQt6.QtWidgets import QWidget, QToolButton, QLabel, QSlider, QPushButton, QStyleOption, QStyle, \
    QLineEdit, QTextEdit

from main_menu_window.config import *
from main_menu_window.pages.ach_menu_page.widgets.current_ach_button import CurrentAchievementButton


class CurrentAchievementInfoPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Page Config
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # Property
        # --- Target Achievement Button
        self.achievement_button = CurrentAchievementButton()  # corresponding achievement button of the info
        # --- Group of LineEdit or TextEdit of info
        self.entry_group = []
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
        self.title_entry = QLineEdit(self)
        self.title_entry.move(14, 144)
        # ------------ read only initially
        self.title_entry.setReadOnly(True)
        # ------------ set editable and close other entry fields when being selected by double click
        self.title_entry.mouseDoubleClickEvent = lambda event: eventHandler(self.title_entry, event)
        # ------------ close other entry fields when being clicked
        self.title_entry.mousePressEvent = lambda event: eventHandler(self.title_entry, event)
        # ------------ change achievement button info when edited : TODO
        self.title_entry.editingFinished.connect(lambda: print("60"))
        # ------------ add to entry group
        self.entry_group.append(self.title_entry)
        # ------ Summary
        # --------- Label
        self.summary_label = QLabel("SUMMARY", self)
        self.summary_label.setStyleSheet("""font-weight: bold;""")
        self.summary_label.move(10, 174)
        # --------- Entry
        self.summary_entry = QLineEdit(self)
        self.summary_entry.move(14, 194)
        # ------------ read only initially
        self.summary_entry.setReadOnly(True)
        # ------------ set editable and close other entry fields when being selected by double click
        self.summary_entry.mouseDoubleClickEvent = lambda event: eventHandler(self.summary_entry, event)
        # ------------ close other entry fields when being clicked
        self.summary_entry.mousePressEvent = lambda event: eventHandler(self.summary_entry, event)
        # ------------ add to entry group
        self.entry_group.append(self.summary_entry)
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
            lambda: self.achievement_button.progress_bar.setValue(self.progress_bar.value()))
        self.progress_bar.move(14, 244)
        # ------ Description
        # --------- Label
        self.description_label = QLabel("DESCRIPTION", self)
        self.description_label.setStyleSheet("""font-weight: bold;""")
        self.description_label.move(10, 274)
        # --------- Entry
        self.description_entry = QTextEdit(self)
        self.description_entry.resize(226, 96)
        self.description_entry.move(14, 294)
        # ------------ read only initially
        self.description_entry.setReadOnly(True)
        # ------------ prevent cursor change to IBeamCursor (default) when read only
        self.description_entry.viewport().setCursor(Qt.CursorShape.ArrowCursor)
        # ------------ set editable and close other entry fields when being selected by double click
        self.description_entry.mouseDoubleClickEvent = lambda event: eventHandler(self.description_entry, event)
        # ------------ close other entry fields when being clicked
        self.description_entry.mousePressEvent = lambda event: eventHandler(self.description_entry, event)
        # ------------ add to entry group
        self.entry_group.append(self.description_entry)

        # Function
        def eventHandler(source, event):
            if event.type() == QEvent.Type.MouseButtonPress or event.type() == QEvent.Type.MouseButtonDblClick:
                for edit in self.entry_group:
                    if edit != source:
                        edit.setReadOnly(True)
                        if isinstance(edit, QTextEdit):
                            print("114")
                            edit.setStyleSheet("""
                                background-color: transparent; 
                                color: white; 
                                border: none; 
                                border-radius: 2px;
                            """)
                if event.type() == QEvent.Type.MouseButtonDblClick:
                    if isinstance(source, QLineEdit):
                        source.setReadOnly(False)
                    elif isinstance(source, QTextEdit):
                        source.setReadOnly(False)
                        source.viewport().setCursor(Qt.CursorShape.IBeamCursor)
                        source.setStyleSheet("""
                            background-color: #484b4f; 
                            color: white; 
                            border: none; 
                            border-radius: 2px;
                        """)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.title_entry.setReadOnly(True)
        self.summary_entry.setReadOnly(True)
        self.description_entry.setReadOnly(True)
        self.description_entry.setStyleSheet("""
            QPlainTextEdit::read-only {
                background-color: transparent;
                color: white;
                border: none;
                border-radius: 1px;
            }
        """)

    def setInfo(self, title, summary, description, achievement_button):
        self.title_entry.setText(title)
        self.title_entry.adjustSize()
        self.summary_entry.setText(summary)
        self.summary_entry.adjustSize()
        self.description_entry.setPlainText(description)
        self.achievement_button = achievement_button

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)
