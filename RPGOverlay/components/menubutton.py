from PyQt6.QtCore import QSize, Qt, QEvent, QPropertyAnimation
from PyQt6.QtGui import QIcon, QCursor, QColor
from PyQt6.QtWidgets import QPushButton, QLabel, QGraphicsColorizeEffect, QToolButton

from RPGOverlay.components.toggle import ToggleWidget
from RPGOverlay.functions import *

class MenuButtonWidget(QPushButton):
    def __init__(self, title="", parent=None, has_toggle=False):
        super().__init__(parent)
        # config
        self.setFixedHeight(50)
        self.setStyleSheet("""
            QPushButton {
                background-color: #28303b;
                font-size: 46pt;
                text-align: left;
                padding: 8px;
            }
            QPushButton::hover {
                background-color: #424d61;
            }
            QPushButton:pressed {
                background-color: #6f6f7d;
            }
        """)
        # Element
        # --- Title
        self.title = QLabel(title, self)
        self.title.setFont(getFont('LeagueGothic-Regular.otf'))
        self.title.setStyleSheet("""color: #d6d6d6;""")
        self.title.move(46, 5)
        # --- Icon
        self.icon = QToolButton(self)
        self.icon.setStyleSheet("""background-color: transparent; border: none;""")
        self.icon.setIcon(QIcon("images/trophy.png"))
        self.icon.setIconSize(QSize(34, 34))
        self.icon.move(6, int(self.height()/2-18))
        self.icon.clicked.connect(self.clicked.emit)
        # --- Toggle
        if has_toggle:
            self.toggle = ToggleWidget(self)
            self.toggle.move(186, 13)
        # Effect
        # --- change curser
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # --- hovering effect
        self.effect = QGraphicsColorizeEffect(self)
        self.effect.setColor(QColor(255, 255, 255))
        self.effect.setStrength(0.1)
        self.setGraphicsEffect(self.effect)
        # Animation
        self.animation = QPropertyAnimation()
        # Event Filter
        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.HoverEnter:
            self.title.setStyleSheet("""color: white;""")
        elif event.type() == QEvent.Type.HoverLeave:
            self.title.setStyleSheet("""color: #d6d6d6;""")

        """
            effect = QGraphicsDropShadowEffect(self)
            effect.setColor(QColor(255, 255, 255))
            effect.setOffset(-1, -1)
            effect.setBlurRadius(20)
            self.setGraphicsEffect(effect)
        """



        return super().eventFilter(source, event)
