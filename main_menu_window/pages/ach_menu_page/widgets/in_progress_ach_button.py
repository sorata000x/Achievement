from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QLabel, QToolButton, QProgressBar

from ..data.achievement_info import AchievementInfo

class InProgressAchievementButton(QPushButton):
    def __init__(self, title="", summary="", description="", parent=None):
        super().__init__(parent)
        # Config
        self.setObjectName("current_achievement_button")
        # Element
        # --- Progress
        self.progress_bar = self.ProgressBar(self)
        self.progress_bar.valueChanged.connect(self.checkStatus)    # check if achievement completed
        # --- Icon
        self.icon = QToolButton(self)
        self.icon.setIcon(QIcon("images/trophy_icon.png"))
        self.icon.setObjectName("icon")
        self.icon.setIconSize(QSize(30, 30))
        self.icon.resize(36, 36)
        self.icon.move(6, 7)
        # --- Title
        self._title = QLabel(title, self)
        self._title.setObjectName("current_achievement_button_title")
        self._title.move(48, 6)
        # --- Summary
        self._summary = QLabel(summary, self)
        self._summary.setObjectName("current_achievement_button_summary")
        self._summary.move(48, 28)
        # --- Description
        self._description = description
        # --- Complete Button
        self.complete_button = QToolButton(self)
        self.complete_button.setIcon(QIcon("images/checkmark.png"))
        self.complete_button.resize(30, 30)
        #   position is set in the resize event
        self.complete_button.hide()
        # --- Delete Button
        self.delete_button = QToolButton(self)
        self.delete_button.setText('✕')
        self.delete_button.resize(16, 16)
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
        self.delete_button.move(int(self.width() - self.delete_button.width()), 0)
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
                    border-radius: 3px;
                }
                QProgressBar:hover {
                    border: 3px solid rgba(84, 116, 156, 200);
                }
                QProgressBar::chunk {
                    background-color: #344f6e;
                    border-top-left-radius: 3px;
                    border-bottom-left-radius: 3px;
                }
            """
            self.setStyleSheet(self.basic_stylesheet)
            self.setFormat('')
            self.move(0, 0)
            self.setMinimum(0)
            self.setMaximum(10)

        def setValue(self, p_int):
            super().setValue(p_int)
            if p_int > self.maximum() * (99 / 100):
                self.setStyleSheet(self.basic_stylesheet + """
                    QProgressBar::chunk {
                        border-radius: 5px;
                    }""")
            else:
                self.setStyleSheet(self.basic_stylesheet + """
                    QProgressBar::chunk {
                        border-top-left-radius: 5px;
                        border-bottom-left-radius: 5px;
                    }""")