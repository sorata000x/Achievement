from PyQt6.QtCore import QPropertyAnimation, QPoint
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget, QGraphicsColorizeEffect, QStyleOption, QStyle, QPushButton

class ToggleWidget(QWidget):
    """ Animated toggle switch widgets_old. """
    def __init__(self, parent=None):
        super().__init__(parent)
        # Config
        self.isOn = False
        self.setStyleSheet("opacity: 0;")
        self.resize(46, 28)
        # Panel
        self.panel = QWidget(self)
        self.panel.setStyleSheet("background-color: #000; border-radius: 4px;")
        self.panel.resize(44, 25)
        # Switch
        self.switch = QWidget(self)
        self.switch.setStyleSheet("background-color: white; border-radius: 3px;")
        self.switch.setGeometry(4, 4, 17, 17)
        # Detector
        self.detector = QWidget(self)
        self.detector.resize(42, 25)
        self.detector.setStyleSheet("opacity: 0;")
        self.detector.mousePressEvent = self.switch_toggle
        # Animation
        #   Switch Pos Anim
        self.switch_anim = QPropertyAnimation(self.switch, b"pos")
        self.switch_anim.setDuration(200)
        #   Color Anim
        effect = QGraphicsColorizeEffect(self.panel)
        effect.setColor(QColor(145, 145, 145))
        self.panel.setGraphicsEffect(effect)
        self.color_anim = QPropertyAnimation(effect, b"color")

    def switch_toggle(self, event):
        if not self.isOn:
            # change toggle color animation
            self.switch_anim.setEndValue(QPoint(22, 4))
            self.switch_anim.start()
            self.color_anim.setEndValue(QColor(114, 194, 114))
            self.color_anim.start()
            # set is on
            self.isOn = True
        else:
            # change toggle color animation
            self.switch_anim.setEndValue(QPoint(4, 4))
            self.switch_anim.start()
            self.color_anim.setEndValue(QColor(145, 145, 145))
            self.color_anim.start()
            # set is off
            self.isOn = False

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)
