from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon

from stylesheet import StyleSheet
from windows.main_menu_window import MainMenuWindow


class Application(QApplication):
    def __init__(self, argv):
        super(Application, self).__init__(argv)
        self.setQuitOnLastWindowClosed(False)
        self.setStyleSheet(StyleSheet)

        # Create the Tray
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon("images/icon.jpg"))
        self.tray.setVisible(True)

        def toggle_menu():
            """
            Show menu window when it is hidden, otherwise hide the window.
            :return:
            """
            if main_menu.isHidden():
                main_menu.move(self.tray.geometry().bottomLeft().x(), self.tray.geometry().bottomLeft().y() + 5)
                main_menu.show()
            else:
                main_menu.hide()
            return

        self.tray.activated.connect(toggle_menu)

        main_menu = MainMenuWindow(self)
