from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QApplication

from RPGOverlay.mainwindow.mainmenuwindow import MainWindow
from .stylesheet import StyleSheet
from RPGOverlay.components.systemtrayicon import SystemTrayIcon


class Application(QApplication):
    def __init__(self, argv):
        super(Application, self).__init__(argv)
        # Window Config
        self.setQuitOnLastWindowClosed(False)
        self.setStyleSheet(StyleSheet)
        # Setting
        self.settings = QSettings('Sora', 'RPGOverlay')
        # Sub Windows
        self.main_menu = MainWindow(self, self.settings)
        # Create the Tray
        self.tray = SystemTrayIcon()
        self.tray.activated.connect(lambda _: self.tray.toggle_window(self.main_menu))
