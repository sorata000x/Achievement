from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QScrollArea, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, \
    QGridLayout

from main_menu_window.config import *
from main_menu_window.functions import getFont
from main_menu_window.widgets.h_line import QHLine
from .achievement_collection_button import AchievementCollectionButton
from .achievement_info_page import AchievementInfoPage


class AchievementCollectionPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Window config
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # set background transparent
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # Properties
        self.achievement_buttons = []   # list of available achievement buttons
        self.current_achievement_button = AchievementCollectionButton()     # current button with the info page
        # Elements
        # --- Background
        self.background = QWidget(self)
        self.background.resize(self.size())
        self.background.setObjectName("panel")
        # --- Back Button
        self.back_button = QPushButton("< Achievements Menu", self)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #437ccc;
            }
            QPushButton::hover {
                color: #7aa6e6;
            }
        """)
        self.back_button.resize(150, 20)
        self.back_button.move(3, 3)
        self.back_button.clicked.connect(self.hide)
        # --- Achievement Collection Label
        self.page_title = QLabel("Collection", self)
        self.page_title.setStyleSheet("""font-size: 26pt; color: white;""")
        self.page_title.setFont(getFont("roboto/Roboto-Thin.ttf"))
        self.page_title.move(64, 30)
        # --- Horizontal Line
        self.h_line = QHLine(self)
        self.h_line.resize(self.width(), 1)
        self.h_line.move(0, 62)
        # Buttons
        # --- Container for scroll area; for resizing
        self.scroll_area_container = QWidget(self)
        self.scroll_area_container.resize(self.width(), 280)
        self.scroll_area_container.move(0, 70)
        # --- Scroll area; contain achievement collection buttons
        self.scroll_area = QScrollArea(self.scroll_area_container)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.horizontalScrollBar().setDisabled(True)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.resize(self.width(), 280)
        # --- Outer container for outer achievement collection buttons layout
        self.achievement_container = QWidget()
        self.achievement_container.setObjectName("panel")
        self.achievement_container.setFixedWidth(self.scroll_area.width()-10)
        #self.achievement_container.move(0, 50)
        self.scroll_area.setWidget(self.achievement_container)
        # --- Outer achievement collection buttons layout
        self.achievement_container_layout = QGridLayout()
        self.achievement_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.achievement_container_layout.setContentsMargins(6, 6, 6, 6)
        self.achievement_container_layout.setSpacing(5)
        self.achievement_container.setLayout(self.achievement_container_layout)
        # Page
        self.achievement_info_page = AchievementInfoPage(self)
        self.achievement_info_page.deleted.connect(self.deleteCurrentAchievementButton)
        self.achievement_info_page.hide()

    def deleteCurrentAchievementButton(self):
        # Remove from the window
        self.achievement_container_layout.removeWidget(self.current_achievement_button)
        self.current_achievement_button.deleteLater()
        # Remove property
        self.achievement_buttons.remove(self.current_achievement_button)
        # Close the page
        self.achievement_info_page.hide()

    def addAchievement(self, achievement_info):
        # Create the achievement collection button
        new_acb = AchievementCollectionButton(achievement_info)
        # Connect button to open info page
        def openCurrentAchievementInfoPage():
            self.current_achievement_button = new_acb
            self.achievement_info_page.setInfo(achievement_info)
            self.achievement_info_page.show()
        new_acb.clicked.connect(openCurrentAchievementInfoPage)

        self.achievement_buttons.append(new_acb)  # Store to button list
        self.placeNewButton(new_acb)    # Display the button

    def placeNewButton(self, button):
        """ Place the button to the achievement container layout. """
        button_count = len(self.achievement_buttons)
        row = (button_count-1) // 4
        col = (button_count-1) % 4
        self.achievement_container_layout.addWidget(button, row, col)
