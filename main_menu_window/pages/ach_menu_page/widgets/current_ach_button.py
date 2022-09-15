from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QLabel, QToolButton, QProgressBar, QStyle


class CurrentAchievementButton(QPushButton):
    def __init__(self, title="", summary="", description="", parent=None):
        super().__init__(parent)
        # Config
        self.setObjectName("current_achievement_button")
        # Element
        # --- Progress
        self.progress_bar = self.ProgressBar(self)
        self.progress_bar.valueChanged.connect(self.checkStatus)
        # --- Title
        self.title = QLabel(title, self)
        self.title.setObjectName("current_achievement_button_title")
        self.title.move(48, 6)
        # --- Icon
        self.icon = QToolButton(self)
        self.icon.setIcon(QIcon("images/trophy_icon.png"))
        self.icon.setObjectName("icon")
        self.icon.setIconSize(QSize(30, 30))
        self.icon.resize(36, 36)
        self.icon.move(6, 7)
        # --- Summary
        self.summary = QLabel(summary, self)
        self.summary.setObjectName("current_achievement_button_summary")
        self.summary.move(48, 28)
        # --- Description
        self.description = description
        # --- Complete button
        self.complete_button = QToolButton(self)
        self.complete_button.setIcon(QIcon("images/checkmark.png"))
        self.complete_button.resize(30, 30)
        self.complete_button.hide()

    def resizeEvent(self, event):
        self.complete_button.move(
            int(self.width() - self.complete_button.width() - 10),
            int(self.height()/2 - self.complete_button.height()/2)
        )
        self.progress_bar.resize(self.width(), self.height())

    def checkStatus(self):
        if self.progress_bar.value() == self.progress_bar.maximum():
            self.complete_button.show()
        else:
            self.complete_button.hide()

    class ProgressBar(QProgressBar):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setObjectName("progress")
            self.setFormat('')
            self.move(0, 0)
            self.setMinimum(0)
            self.setMaximum(10)

        def setValue(self, p_int):
            super().setValue(p_int)
            if p_int > self.maximum() * (99 / 100):
                self.setStyleSheet("""
                    #progress::chunk {
                        border-radius: 5px;
                    }""")
            else:
                self.setStyleSheet("""
                    #progress::chunk {
                        border-top-left-radius: 5px;
                        border-bottom-left-radius: 5px;
                    }""")