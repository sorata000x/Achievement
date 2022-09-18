from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QSize, Qt, QPoint, QEvent, QObject
from PyQt6.QtGui import QIcon, QPainter
from PyQt6.QtWidgets import QWidget, QToolButton, QLabel, QSlider, QPlainTextEdit, QPushButton, QStyleOption, QStyle, \
    QGraphicsDropShadowEffect, QLineEdit, QTextEdit

from main_menu_window.config import *
from main_menu_window.pages.ach_menu_page.widgets.current_ach_button import CurrentAchievementButton


class CurrentAchievementInfoPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Config
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # --- Target Achievement Button
        self.achievement_button = CurrentAchievementButton()  # corresponding achievement button of the info
        # Animation
        self.sliding_page_anim = QPropertyAnimation(self, b"pos")
        self.sliding_page_anim.setEasingCurve(QEasingCurve.Type.OutCurve)

        self.edit_group = []
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
        self.title_entry = QLineEdit(self)
        self.title_entry.setReadOnly(True)
        self.title_entry.mouseDoubleClickEvent = lambda event: eventHandler(self.title_entry, event)
        self.edit_group.append(self.title_entry)
        self.title_entry.move(14, 144)
        # --- Summary
        # ------ label
        self.summary_label = QLabel("SUMMARY", self)
        self.summary_label.setStyleSheet("""font-weight: bold;""")
        self.summary_label.move(10, 174)
        # ------ text
        self.summary_entry = QLineEdit(self)
        self.summary_entry.setReadOnly(True)
        self.summary_entry.mouseDoubleClickEvent = lambda event: eventHandler(self.summary_entry, event)
        self.edit_group.append(self.summary_entry)
        self.summary_entry.move(14, 194)
        # --- Progress
        # ------ label
        self.progress_label = QLabel("PROGRESS", self)
        self.progress_label.setStyleSheet("""font-weight: bold;""")
        self.progress_label.move(10, 224)
        # ------ bar
        self.progress_bar = QSlider(Qt.Orientation.Horizontal, self)
        self.progress_bar.setObjectName("info_progress")
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(10)
        self.progress_bar.setFixedWidth(225)
        self.progress_bar.valueChanged.connect(
            lambda _: self.achievement_button.progress_bar.setValue(self.progress_bar.value()))
        self.progress_bar.move(14, 244)
        # --- Description
        # ------ label
        self.description_label = QLabel("DESCRIPTION", self)
        self.description_label.setStyleSheet("""font-weight: bold;""")
        self.description_label.move(10, 274)
        # ------ field
        self.description_field = QTextEdit(self)
        self.description_field.setReadOnly(True)
        self.description_field.resize(226, 96)
        self.description_field.move(14, 290)
        self.edit_group.append(self.description_field)
        self.description_field.mouseDoubleClickEvent = lambda event: eventHandler(self.description_field, event)

        # Function
        def eventHandler(source, event):
            if event.type() == QEvent.Type.MouseButtonPress or event.type() == QEvent.Type.MouseButtonDblClick:
                for edit in self.edit_group:
                    if edit != source:
                        edit.setReadOnly(True)
                if event.type() == QEvent.Type.MouseButtonDblClick:
                    if isinstance(source, QLineEdit):
                        source.setReadOnly(False)
                    elif isinstance(source, QTextEdit):
                        source.setReadOnly(False)
                        source.setStyleSheet("""
                            background-color: #484b4f; 
                            color: white; border: none; 
                            border-radius: 2px;
                        """)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.title_entry.setReadOnly(True)
        self.summary_entry.setReadOnly(True)
        self.description_field.setReadOnly(True)
        self.description_field.setStyleSheet("""
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
