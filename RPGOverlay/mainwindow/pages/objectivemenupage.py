from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QScrollArea, QVBoxLayout, QLabel

from config import *
from RPGOverlay.functions import getFont
from RPGOverlay.data.objectiveinfo import AchievementInfo
from RPGOverlay.mainwindow.pages.collectionpage import AchievementCollectionPage
from .createobjectivepage import CreateAchievementPage
from RPGOverlay.mainwindow.pages.objectiveinfopage import InProgressAchievementInfoPage
from ...components.objectivebutton import InProgressAchievementButton
from ...components.createbutton import CreateNewButtonWidget
from ...components.hline import QHLine
from ...components.menubutton import MenuButtonWidget
from ...components.scrollarea import ScrollArea

class AchievementMenuPage(QWidget):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        # Config
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # Properties
        self.in_progress_achievement_buttons = settings.value(      # list of available achievement buttons
            'in_progress_achievement_buttons', [], InProgressAchievementButton)
        self.current_achievement_button = InProgressAchievementButton()     # current button with the info page
        # Elements
        # --- Background
        self.background = QWidget(self)
        self.background.resize(self.size())
        self.background.setObjectName("panel")
        # --- Back Button
        self.back_button = QPushButton("< Tool menu", self)
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
        self.back_button.resize(80, 20)
        self.back_button.move(3, 3)
        self.back_button.clicked.connect(self.hide)
        # --- Achievement Label
        self.achievement_label = QLabel("Achievement", self)
        self.achievement_label.setStyleSheet("""font-size: 26pt; color: #dbdbdb;""")
        self.achievement_label.setFont(getFont("roboto/Roboto-Thin.ttf"))
        self.achievement_label.move(int(self.width()/2-76), 30)
        # --- Horizontal Line
        self.h_line = QHLine(self)
        self.h_line.setStyleSheet("""border: 1px solid #dbdbdb;""")
        self.h_line.resize(self.width(), 1)
        self.h_line.move(0, 62)
        # ------ Achievement Collection Button
        self.achievement_collection_button = MenuButtonWidget("Collection", self)
        self.achievement_collection_button.setFixedWidth(self.width())
        self.achievement_collection_button.setFixedHeight(50)
        self.achievement_collection_button.move(0, 68)
        # --- Achievements Buttons
        # ------ Widget to contain scroll area; for resizing
        self.ab_scroll_area_container = QWidget(self)
        self.ab_scroll_area_container.resize(self.width(), self.height()-150)
        self.ab_scroll_area_container.move(0, 118)
        # ------ Scroll Area, to contain buttons
        self.ab_scroll_area = ScrollArea(self.ab_scroll_area_container)
        #self.ab_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ab_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ab_scroll_area.setWidgetResizable(True)
        self.ab_scroll_area.resize(self.width(), self.ab_scroll_area_container.height())
        self.ab_scroll_area.move(0, 3)
        self.ab_scroll_area.setContentsMargins(0, 0, 0, 0)
        # --------- Widget to contain created achievement buttons layout
        self.cab_widget = QWidget()
        self.cab_widget.setFixedWidth(self.ab_scroll_area.width())
        # ------------ adjust size respond to scroll bar
        self.ab_scroll_area.verticalScrollBar().showed.connect(
            lambda: self.cab_widget.setFixedWidth(self.ab_scroll_area.width()-16))
        self.ab_scroll_area.verticalScrollBar().hided.connect(
            lambda: self.cab_widget.setFixedWidth(self.ab_scroll_area.width()))
        self.cab_widget.setObjectName("panel")
        self.ab_scroll_area.setWidget(self.cab_widget)
        # --------- Layout
        self.cab_layout = QVBoxLayout()
        self.cab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cab_layout.setContentsMargins(0, 0, 0, 0)
        self.cab_layout.setSpacing(4)
        self.cab_widget.setLayout(self.cab_layout)
        # --------- Create New Button: always at bottom
        self.create_new_button = CreateNewButtonWidget()
        self.cab_layout.addWidget(self.create_new_button)
        # Pages
        # --- Create-New Page
        self.create_new_page = CreateAchievementPage(self)
        self.create_new_page.clear()
        self.create_new_page.hide()
        self.create_new_page.ok_button.clicked.connect(
            lambda: self.create_new_achievement(self.create_new_page.achievement_info))
        self.create_new_button.clicked.connect(self.create_new_page.show)
        # --- Current Achievement Info Page
        self.in_progress_achievement_info_page = InProgressAchievementInfoPage(self)
        self.in_progress_achievement_info_page.hide()
        self.in_progress_achievement_info_page.deleted.connect(self.deleteCurrentAchievementButton)
            # delete the current achievement button if deletion occur in the info page
        # --- Achievement Collection Page
        self.ach_collection_page = AchievementCollectionPage(self)
        self.ach_collection_page.hide()
        self.achievement_collection_button.clicked.connect(self.ach_collection_page.show)
        # Settings
        """
        self.settings = settings
        if self.settings.contains(f'{self.__class__.__name__}-cab_layout'):
            self.cab_layout = self.settings.value(f'{self.__class__.__name__}-cab_layout')
        if self.settings.contains(f'{self.__class__.__name__}-in_progress_achievement_buttons'):
            self.in_progress_achievement_buttons = self.settings.value(
                f'{self.__class__.__name__}-in_progress_achievement_buttons')
        """

    # Page Function

    def move(self, x, y):
        """ Move sub-main_menu_window as well."""
        super().move(x, y)
        self.ach_collection_page.move(x, y)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        #if event.key() == Qt.Key.Key_Return:
        #    self.create_new_achievement()

    # Element Function

    def deleteCurrentAchievementButton(self):
        # Remove from the window
        self.cab_layout.removeWidget(self.current_achievement_button)
        self.current_achievement_button.deleteLater()
        # Remove property
        self.in_progress_achievement_buttons.remove(self.current_achievement_button)
        # Close the page
        self.in_progress_achievement_info_page.hide()
        # Record change
        self.settings.setValue(f'{self.__class__.__name__}-cab_layout', self.cab_layout)
        self.settings.setValue(
            f'{self.__class__.__name__}-in_progress_achievement_buttons', self.in_progress_achievement_buttons)

    def create_new_achievement(self, achievement_info):
        # Create achievement button
        new_achievement_button = InProgressAchievementButton(achievement_info)   # create a new button

        def openInProgressAchievementPage(info):
            self.current_achievement_button = new_achievement_button    # set the current achievement button
            self.in_progress_achievement_info_page.setInfo(info)    # set the info to the page
            self.in_progress_achievement_info_page.show()   # open the page
        new_achievement_button.clicked.connect(
            lambda: openInProgressAchievementPage(new_achievement_button.achievement_info))
        # Connect complete function to achievement completed.
        def delete():
            # Remove from the window
            self.cab_layout.removeWidget(new_achievement_button)
            new_achievement_button.deleteLater()
            # Remove the property
            self.in_progress_achievement_buttons.remove(new_achievement_button)
        def complete(achievement_info):
            """ Triggered after achievement marked complete. """
            # Add achievement to collection page
            self.ach_collection_page.addAchievement(achievement_info)
            # And then delete it
            delete()
        new_achievement_button.complete_button.clicked.connect(
            lambda: complete(new_achievement_button.achievement_info))
        # Add to button list
        self.in_progress_achievement_buttons.append(new_achievement_button)
        # Insert button in the layout
        last_index = self.cab_layout.indexOf(self.create_new_button)
        self.cab_layout.insertWidget(last_index, new_achievement_button)
        self.create_new_page.clear()
        self.create_new_page.hide()

        # Record change
        """
        self.settings.setValue(f'{self.__class__.__name__}-cab_layout', self.cab_layout)
        self.settings.setValue(
            f'{self.__class__.__name__}-in_progress_achievement_buttons', self.in_progress_achievement_buttons)
        """