from PyQt6.QtCore import pyqtSignal, QObject


class AchievementInfo(QObject):
    changed = pyqtSignal()

    def __init__(self, title="", summary="", description="", progress=0):
        super().__init__()
        self._title = title
        self._summary = summary
        self._description = description
        self._progress = progress

    # ACCESSOR

    def title(self):
        return self._title

    def summary(self):
        return self._summary

    def description(self):
        return self._description

    def progress(self):
        return self._progress

    # MUTATOR

    def setTitle(self, new_title: str):
        self._title = new_title
        self.changed.emit()     # emit changed signal

    def setSummary(self, new_summary: str):
        self._summary = new_summary
        self.changed.emit()     # emit changed signal

    def setDescription(self, new_description: str):
        self._description = new_description
        self.changed.emit()     # emit changed signal

    def setProgress(self, value: int):
        self._progress = value
        self.changed.emit()     # emit changed signal
