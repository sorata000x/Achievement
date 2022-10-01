from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtWidgets import QWidget, QPushButton, QScrollArea, QVBoxLayout, QLabel

from main_menu_window.functions import getFont
from main_menu_window.pages.ach_menu_page.pages.create_new_page import CreateNewPage
from main_menu_window.pages.ach_menu_page.pages.in_progress_ach_info_page import CurrentAchievementInfoPage
from main_menu_window.config import *
from main_menu_window.pages.ach_menu_page.widgets.in_progress_ach_button import InProgressAchievementButton
from main_menu_window.widgets.h_line import QHLine
from main_menu_window.widgets.menu_button import MenuButtonWidget
from main_menu_window.widgets.create_new_button import CreateNewButtonWidget
from main_menu_window.pages.ach_menu_page.pages.ach_collection_page.ach_collection_page import AchievementCollectionPage

class AchievementMenuPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Config
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # Elements
        # --- Background
        self.background = QWidget(self)
        self.background.resize(self.size())
        self.background.setObjectName("panel")
        # --- Back Button
        self.back_button = QPushButton("< Tool menu", self)
        self.back_button.setObjectName("back_button")
        self.back_button.resize(80, 20)
        self.back_button.move(3, 3)
        self.back_button.clicked.connect(self.hide)
        # --- Achievement Label
        self.achievement_label = QLabel("Achievement", self)
        self.achievement_label.setStyleSheet("""font-size: 26pt; color: white;""")
        self.achievement_label.setFont(getFont("roboto/Roboto-Thin.ttf"))
        self.achievement_label.move(54, 30)
        # --- Horizontal Line
        self.h_line = QHLine(self)
        self.h_line.resize(self.width() - 20, 1)
        self.h_line.move(10, 62)
        # ------ Achievement Collection Button
        self.achievement_collection_button = MenuButtonWidget("Collection", self)
        self.achievement_collection_button.setFixedWidth(self.width()-31)
        self.achievement_collection_button.setFixedHeight(50)
        self.achievement_collection_button.move(14, 74)
        # --- Achievements Buttons
        # ------ Widget to contain scroll area; for resizing
        self.ab_scroll_area_container = QWidget(self)
        self.ab_scroll_area_container.resize(self.width()-10, 256)
        self.ab_scroll_area_container.move(14, 128)
        # ------ Scroll Area, to contain buttons
        self.ab_scroll_area = QScrollArea(self.ab_scroll_area_container)
        self.ab_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ab_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ab_scroll_area.setWidgetResizable(True)
        self.ab_scroll_area.resize(self.width()-14, 256)
        self.ab_scroll_area.move(0, 3)
        self.ab_scroll_area.setContentsMargins(0, 0, 0, 0)
        # --------- Widget to contain created achievement buttons layout
        self.cab_widget = QWidget()
        self.cab_widget.setFixedWidth(self.ab_scroll_area.width()-16)
        self.cab_widget.setObjectName("panel")
        self.ab_scroll_area.setWidget(self.cab_widget)
        # --------- Layout
        self.cab_layout = QVBoxLayout()
        self.cab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cab_layout.setContentsMargins(0, 0, 0, 0)
        self.cab_layout.setSpacing(14)
        self.cab_widget.setLayout(self.cab_layout)
        # --------- Create New Button: always at bottom
        self.create_new_button = CreateNewButtonWidget()
        self.cab_layout.addWidget(self.create_new_button)
        # --------- Current Achievement Buttons
        self.current_achievement_buttons = []
        # Pages
        # --- Create-New Page
        self.create_new_page = CreateNewPage(self)
        self.create_new_page.clear()
        self.create_new_page.hide()
        self.create_new_page.ok_button.clicked.connect(
            lambda _: self.create_new_achievement(
                self.create_new_page.title_entry.text(),
                self.create_new_page.summary_entry.text(),
                self.create_new_page.description_entry.text()
            )
        )
        self.create_new_button.clicked.connect(self.create_new_page.show)
        # --- Current Achievement Info Page
        self.in_progress_achievement_info_page = CurrentAchievementInfoPage(self)
        self.in_progress_achievement_info_page.hide()
        # --- Achievement Collection Page
        self.ach_collection_page = AchievementCollectionPage(self)
        self.ach_collection_page.hide()
        self.achievement_collection_button.clicked.connect(self.ach_collection_page.show)

        if debug:
            self.create_new_achievement("Title", "Summary", "Description")

    def move(self, x, y):
        """ Move sub-main_menu_window as well."""
        super().move(x, y)
        self.ach_collection_page.move(x, y)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        #if event.key() == Qt.Key.Key_Return:
        #    self.create_new_achievement()

    def showInProgressAchievementPage(self, achievement_info):
        self.in_progress_achievement_info_page.setInfo(achievement_info)
        self.in_progress_achievement_info_page.show()

    def create_new_achievement(self, title, summary, description):
        # Create achievement button
        new_achievement_button = InProgressAchievementButton(title, summary, description)   # create a new button
        new_achievement_button.clicked.connect(
            lambda: self.showInProgressAchievementPage(new_achievement_button.achievement_info))
        # Connect complete function to achievement completed.
        def complete(achievement):
            """ Triggered after achievement marked complete. """
            # Add achievement to collection page
            self.ach_collection_page.addAchievement(
                achievement.title(), achievement.summary(), achievement.description())
            # Remove achievement button from menu
            self.cab_layout.removeWidget(new_achievement_button)
            new_achievement_button.deleteLater()
            self.current_achievement_buttons.remove(new_achievement_button)
        new_achievement_button.complete_button.clicked.connect(lambda: complete(new_achievement_button.achievement_info))
        # Add to button list
        self.current_achievement_buttons.append(new_achievement_button)
        # Insert button in the layout
        last_index = self.cab_layout.indexOf(self.create_new_button)
        self.cab_layout.insertWidget(last_index, new_achievement_button)
        self.create_new_page.clear()
        self.create_new_page.hide()

