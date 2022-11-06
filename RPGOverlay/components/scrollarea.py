from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QScrollArea, QScrollBar


class ScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setVerticalScrollBar(VerticalScrollBar())

class VerticalScrollBar(QScrollBar):
    showed = pyqtSignal()
    hided = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def showEvent(self, event):
        super().showEvent(event)
        self.showed.emit()

    def hideEvent(self, event):
        self.hided.emit()
        super().hideEvent(event)