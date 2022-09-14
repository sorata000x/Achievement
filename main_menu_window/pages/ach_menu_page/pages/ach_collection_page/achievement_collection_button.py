from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QToolButton


class AchievementCollectionButton(QToolButton):
    """ Achievement collection button represent by an icon button. """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Config
        self.resize(45, 45)
        self.move(10, 60)
        # Icon
        self.setIcon(QIcon("images/trophy_icon.png"))
        self.setObjectName("icon")
        self.setIconSize(self.size())
