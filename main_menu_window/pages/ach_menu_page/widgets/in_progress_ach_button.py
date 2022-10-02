from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QLabel, QToolButton, QProgressBar

from ..data.achievement_info import AchievementInfo

class InProgressAchievementButton(QPushButton):
    def __init__(self, title="", summary="", description="", parent=None):
        super().__init__(parent)
        # Config
        self.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: black;
                height: 34px;
                text-align: left;
                padding: 8px;
            }
        """)
        # Element
        # --- Progress
        self.progress_bar = self.ProgressBar(self)
        self.progress_bar.valueChanged.connect(self.checkStatus)    # check if achievement completed
        # --- Icon
        self.icon = QToolButton(self)
        self.icon.setStyleSheet("""
            background-color: black;
            border: none;
        """)
        self.icon.setContentsMargins(0, 0, 0, 0)
        self.icon.resize(QSize(38, 38))
        self.icon.setIcon(QIcon("images/trophy_icon.png"))
        self.icon.setIconSize(QSize(28, 28))
        self.icon.move(6, 7)
        # --- Title
        self._title = QLabel(title, self)
        self._title.setStyleSheet("""
            background-color: transparent;
            color: white;
            font-size: 16pt;
        """)
        self._title.move(48, 8)
        # --- Summary
        self._summary = QLabel(summary, self)
        self._summary.setStyleSheet("""
            background-color: transparent;
            color: white;
            font-size: 12pt;
        """)
        self._summary.move(48, 28)
        # --- Description
        self._description = description
        # --- Complete Button
        self.complete_button = QToolButton(self)
        self.complete_button.setIcon(QIcon("images/checkmark.png"))
        self.complete_button.resize(30, 30)
        #   position is set in the resize event
        self.complete_button.hide()
        #   position is set in the resize event
        # Achievement Data
        self.achievement_info = AchievementInfo(title, summary, description, progress=0)
        self.achievement_info.changed.connect(lambda: self.setInfo(self.achievement_info))

    # MUTATOR

    def title(self):
        return self._title.text()

    def summary(self):
        return self._summary.text()

    def description(self):
        return self._description.title()

    # ACCESSOR

    def setTitle(self, new_title):
        self._title.setText(new_title)
        self._title.adjustSize()

    def setSummary(self, new_summary):
        self._summary.setText(new_summary)
        self._summary.adjustSize()

    def setDescription(self, new_description):
        self._description = new_description

    def setProgress(self, new_value):
        self.progress_bar.setValue(new_value)

    def setInfo(self, new_achievement_info):
        self.setTitle(new_achievement_info.title())
        self.setSummary(new_achievement_info.summary())
        self.setDescription(new_achievement_info.description())
        self.setProgress(new_achievement_info.progress())

    # EVENT

    def resizeEvent(self, event):
        self.complete_button.move(
            int(self.width() - self.complete_button.width() - 17),
            int(self.height() / 2 - self.complete_button.height() / 2)
        )
        self.progress_bar.resize(self.width(), self.height())

    # Function

    def checkStatus(self):
        """ Check if the achievement is completed or not """
        if self.progress_bar.value() == self.progress_bar.maximum():
            self.complete_button.show()
        else:
            self.complete_button.hide()

    # Widget

    class ProgressBar(QProgressBar):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.basic_stylesheet = """
                QProgressBar {
                    text-align: center;
                    border: 0;
                    background-color: #202429;
                }
                QProgressBar:hover {
                    border: 3px solid rgba(84, 116, 156, 200);
                }
                QProgressBar::chunk {
                    background-color: #344f6e;
                }
            """
            self.setStyleSheet(self.basic_stylesheet)
            self.setFormat('')
            self.move(0, 0)
            self.setMinimum(0)
            self.setMaximum(10)
