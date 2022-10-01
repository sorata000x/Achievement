from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QLabel, QToolButton, QGridLayout, QScrollArea, QPushButton, QSpacerItem, \
    QSizePolicy, QHBoxLayout, QVBoxLayout
from main_menu_window.config import *
from main_menu_window.functions import getFont
from main_menu_window.pages.ach_menu_page.widgets.in_progress_ach_button import InProgressAchievementButton
from main_menu_window.pages.ach_menu_page.pages.in_progress_ach_info_page import CurrentAchievementInfoPage
from main_menu_window.widgets.h_line import QHLine
from .achievement_collection_button import AchievementCollectionButton
from .achievement_info import AchievementInfo
from .achievement_info_page import AchievementInfoPage

class AchievementCollectionPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Window config
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # set background transparent
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # Elements
        # --- Background
        self.background = QWidget(self)
        self.background.resize(self.size())
        self.background.setObjectName("panel")
        # --- Back Button
        self.back_button = QPushButton("< Achievements Menu", self)
        self.back_button.setObjectName("back_button")
        self.back_button.resize(150, 20)
        self.back_button.move(3, 3)
        self.back_button.clicked.connect(self.hide)
        # --- Achievement Collection Label
        self.ach_collection_label = QLabel("Collection", self)
        self.ach_collection_label.setStyleSheet("""font-size: 26pt; color: white;""")
        self.ach_collection_label.setFont(getFont("roboto/Roboto-Thin.ttf"))
        self.ach_collection_label.move(70, 30)
        # --- Horizontal Line
        self.h_line = QHLine(self)
        self.h_line.resize(self.width() - 20, 1)
        self.h_line.move(10, 62)
        # Buttons
        # --- Container for scroll area; for resizing
        self.acb_scroll_area_container = QWidget(self)
        self.acb_scroll_area_container.resize(self.width()-10, 280)
        self.acb_scroll_area_container.move(10, 74)
        # --- Scroll area; contain achievement collection buttons
        self.acb_scroll_area = QScrollArea(self.acb_scroll_area_container)
        self.acb_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.acb_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.acb_scroll_area.setWidgetResizable(True)
        self.acb_scroll_area.resize(self.width()-10, 280)
        # --- Outer container for outer achievement collection buttons layout
        self.acb_outer_container = QWidget()
        self.acb_outer_container.setObjectName("panel")
        self.acb_outer_container.move(0, 50)
        self.acb_scroll_area.setWidget(self.acb_outer_container)
        # --- Outer achievement collection buttons layout
        self.acb_outer_layout = QVBoxLayout()
        self.acb_outer_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.acb_outer_layout.setContentsMargins(0, 0, 0, 0)
        self.acb_outer_container.setLayout(self.acb_outer_layout)
        # --- Inner container for achievement collection button layout
        self.acb_inner_container = QWidget()
        self.acb_inner_container.setMaximumHeight(100)
        self.acb_outer_layout.addWidget(self.acb_inner_container)
        # --- Inner achievement collection button layout
        self.acb_inner_layout = QHBoxLayout()
        self.acb_inner_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.acb_inner_layout.setContentsMargins(8, 8, 8, 8)
        self.acb_inner_container.setLayout(self.acb_inner_layout)

        """
        self.acb_layout = QGridLayout()
        spacerItem = QSpacerItem(   # row spacing
            20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )  # QSpacerItem(w, h[, hData=QSizePolicy.Minimum[, vData=QSizePolicy.Minimum]])¶
        self.acb_layout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)  # column spacing
        self.acb_layout.addItem(spacerItem1, 1, 1, 1, 1)
        """
# TESTING
        if False:
            for i in range(5):
                for j in range(4):
                    self.acb_inner_layout.addWidget(self.AchievementCollectionButton(), i, j)
# -------
        #self.acb_container.setLayout(self.acb_inner_layout)

        self.achievement_buttons = []

        # Page
        self.achievement_info_page = AchievementInfoPage(self)
        self.achievement_info_page.hide()

    def addAchievement(self, title, summary, description):
        new_acb = AchievementCollectionButton()
        self.achievement_buttons.append(new_acb)    # Store to button list
        self.acb_inner_layout.addWidget(new_acb)    # Display in button layout
        # Connect button to open info page
        def openCurrentAchievementInfoPage():
            self.achievement_info_page.setInfo(title, summary, description)
            self.achievement_info_page.show()
        new_acb.clicked.connect(openCurrentAchievementInfoPage)


