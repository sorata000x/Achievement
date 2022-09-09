from PyQt6.QtWidgets import QPushButton


class CreateNewButtonWidget(QPushButton):
    """ Button widgets to suggest creating new widgets. """
    def __init__(self, parent=None):
        super().__init__("Create New +", parent)
        # Config
        self.setObjectName("create_new_button")
