from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QPushButton

from config import *


class DeleteConfirmBox(QWidget):
    """ Pop-up message box to confirm if the user going to delete something. """
    def __init__(self, parent=None):
        super().__init__(parent)
        # Config
        self.resize(WINDOW_WIDTH-20, 90)
        # Element
        # --- Background
        self.background = QWidget(self)
        self.background.resize(self.size())
        self.background.setStyleSheet("""
            background-color: rgba(0, 0, 0, 235);
            border-radius: 5px;
        """)
        # --- Message
        self.message = QPlainTextEdit(self)
        self.message.setPlainText("Are you sure you want to delete this achievement?")
        self.message.setStyleSheet("""
            background-color: transparent; 
            color: white; 
            font-size: 14pt;
        """)
        self.message.move(6, 10)
        self.message.setFixedWidth(self.width()-10)
        self.message.setDisabled(True)
        # --- Cancel Button
        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("Cancel")
        self.cancel_button.setStyleSheet("""
            background-color: #53668a;
            color: white;
            border: none;
            border-radius: 3px;
        """)
        self.cancel_button.clicked.connect(self.hide)
        self.cancel_button.resize(60, 20)
        self.cancel_button.move(90, 60)
        # --- Delete Button
        self.delete_button = QPushButton(self)
        self.delete_button.setText("Delete")
        self.delete_button.setStyleSheet("""
            background-color: white;
            border: none;
            border-radius: 3px;
        """)
        self.delete_button.clicked.connect(self.hide)
        self.delete_button.resize(50, 20)
        self.delete_button.move(160, 60)
