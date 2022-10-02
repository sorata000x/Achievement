from PyQt6.QtWidgets import QPushButton


class CreateNewButtonWidget(QPushButton):
    """ Button widgets to suggest creating new widgets. """
    def __init__(self, parent=None):
        super().__init__("Create New +", parent)
        # Config
        self.setStyleSheet("""
            QPushButton {
                border: 1px solid #676d75;
                color: rgba(255, 255, 255, 100);
                height: 34px;
                font-size: 20pt;
                text-align: center;
                padding: 8px;
            }
            QPushButton::hover {
                border: 5px solid #585d64;
                background-color: #555a61;
            }
        """)
