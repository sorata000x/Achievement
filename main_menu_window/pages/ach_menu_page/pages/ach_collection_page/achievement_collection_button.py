from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QToolButton, QWidget

from main_menu_window.pages.ach_menu_page.data.achievement_info import AchievementInfo


class AchievementCollectionButton(QToolButton):
    """ Achievement collection button represent by an icon button. """

    def __init__(self, achievement_info=AchievementInfo(), parent=None):
        super().__init__(parent)
        # Config
        self.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border-radius: 3px;
                border: 3px solid transparent;
            }
            QToolButton::hover {
                border: 3px solid #707780;
            }
        """)
        self.setFixedSize(QSize(50, 50))

        # Icon
        self.setIcon(QIcon(achievement_info.image()))
        self.setIconSize(self.size())
