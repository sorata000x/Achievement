from PyQt6.QtCore import pyqtSignal, QObject
from config import *

class AchievementInfo(QObject):
    changed = pyqtSignal()

    def __init__(self, image=DEFAULT_IMAGE, title="", summary="", description="", progress=0):
        super().__init__()

        self._image = image
        self._title = title
        self._summary = summary
        self._description = description
        self._progress = progress

    # ACCESSOR

    def image(self):
        return self._image

    def title(self):
        return self._title

    def summary(self):
        return self._summary

    def description(self):
        return self._description

    def progress(self):
        return self._progress

    # MUTATOR

    def setInfo(self, new_image, new_title, new_summary, new_description):
        self._image = new_image
        self._title = new_title
        self._summary = new_summary
        self._description = new_description

    def setImage(self, new_image):
        self._image = new_image
        self.changed.emit()     # emit changed signal

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


