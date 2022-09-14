from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon

from stylesheet import StyleSheet
from main_menu_window.main_menu_window import MainWindow


class Application(QApplication):
    def __init__(self, argv):
        super(Application, self).__init__(argv)
        # Window Config
        self.setQuitOnLastWindowClosed(False)
        self.setStyleSheet(StyleSheet)
        # Sub Windows
        self.main_menu = MainWindow(self)
        # Create the Tray
        self.tray = SystemTrayIcon()
        self.tray.activated.connect(lambda _: self.tray.toggle_window(self.main_menu))

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.setIcon(QIcon("images/icon.jpg"))
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


