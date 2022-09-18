from PyQt6.QtCore import QPropertyAnimation


class Animation:
    def __init__(self):
        self.color_anim = QPropertyAnimation()

    def glowEffect(self, target, color):
        self.color_anim.setTargetObject(target)
        self.color_anim.setPropertyName(b"color")
        self.color_anim.setDuration(100)
        self.color_anim.setEndValue(color)
        self.color_anim.start()

