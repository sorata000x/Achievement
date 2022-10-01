from PyQt6.QtWidgets import QApplication

from main_menu_window.main_menu_window import MainWindow
from stylesheet import StyleSheet
from widgets.system_tray_icon import SystemTrayIcon


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
