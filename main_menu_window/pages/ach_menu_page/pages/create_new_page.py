from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QSize, QPoint
from PyQt6.QtGui import QIcon, QFontMetricsF
from PyQt6.QtWidgets import QWidget, QToolButton, QLabel, QLineEdit, QPlainTextEdit, QPushButton

from main_menu_window.config import *


class CreateNewPage(QWidget):
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
        self.back_button.setObjectName("back_button")
        self.back_button.resize(50, 20)
        self.back_button.move(3, 3)
        self.back_button.clicked.connect(self.hide)
        # --- Image Upload Button
        self.image_upload_button = QToolButton(self.background)
        self.image_upload_button.setIcon(QIcon("images/trophy_icon.png"))
        self.image_upload_button.setIconSize(QSize(60, 60))
        self.image_upload_button.move(10, 40)
        # --- Title Entry
        self.title_label = QLabel("TITLE", self.background)
        self.title_label.move(10, 120)
        self.title_entry = QLineEdit(self.background)
        self.title_entry.move(10, 140)
        self.title_entry.resize(222, 24)
        self.title_entry.setStyleSheet("""
                    background-color: #2b2b2b; 
                    border: 0; border-radius: 2px; 
                    padding: 2px; 
                    color: white;
                    """)
        # Summary Entry
        self.summary_label = QLabel("SUMMARY", self.background)
        self.summary_label.move(10, 170)
        self.summary_entry = QLineEdit(self.background)
        self.summary_entry.resize(222, 24)
        self.summary_entry.move(10, 190)
        self.summary_entry.setStyleSheet("""
                    background-color: #2b2b2b; 
                    border: 0; border-radius: 2px; 
                    padding: 2px; 
                    color: white;
                    """)
        # Description
        # --- Label
        self.description_label = QLabel("DESCRIPTION", self.background)
        self.description_label.move(10, 220)
        # --- Entry
        self.description_entry = QPlainTextEdit(self.background)
        self.description_entry.move(10, 240)
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
        self.cancel_button.move(94, 360)
        self.cancel_button.setStyleSheet("""
                    background-color: #636363;
                    border-radius: 2px;
                    color: white;
                """)
        self.cancel_button.clicked.connect(self.hide)
        # OK Button
        self.ok_button = QPushButton("OK", self.background)
        self.ok_button.resize(66, 24)
        self.ok_button.move(170, 360)
        self.ok_button.setStyleSheet("""
                    background-color: #198cff;
                    border-radius: 2px;
                    color: white;
                """)

    def clear(self):
        self.title_entry.clear()
        self.summary_entry.clear()
        self.description_entry.clear()

    def sliding_page_in(self):
        self.sliding_page_anim.setDuration(300)
        self.sliding_page_anim.setEndValue(QPoint(0, 0))
        self.sliding_page_anim.start()

    def sliding_page_out(self):
        self.sliding_page_anim.setDuration(100)
        self.sliding_page_anim.setEndValue(QPoint(self.width(), 0))
        self.sliding_page_anim.start()