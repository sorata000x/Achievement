from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QSystemTrayIcon
from config import *

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        iconpath = os.path.join(BASEDIR, 'images/icon.jpg')
        self.setIcon(QIcon(iconpath))
        self.setVisible(True)

    def toggle_window(self, window):
        """
        Show menu window when it is hidden, otherwise hide the window.
        :return:
        """
        if window.isHidden():
            window.move(self.geometry().bottomLeft().x(), self.geometry().bottomLeft().y() + 5)
            window.show()
        else:
            window.hide()
        return
