from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtWidgets import QWidget, QPushButton, QScrollArea, QVBoxLayout, QLabel

from main_menu_window.pages.ach_menu_page.pages.create_new_page import CreateNewPage
from main_menu_window.pages.ach_menu_page.pages.current_ach_info_page import CurrentAchievementInfoPage
from main_menu_window.config import *
from main_menu_window.pages.ach_menu_page.widgets.current_ach_button import CurrentAchievementButton
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
        self.achievement_label.setStyleSheet(""" font-size: 26pt """)
        self.achievement_label.move(54, 24)
        # --- Horizontal Line
        self.h_line = QHLine(self)
        self.h_line.resize(self.width() - 20, 10)
        self.h_line.move(10, 56)
        # ------ Achievement Collection Button
        self.achievement_collection_button = MenuButtonWidget("Collection", self)
        self.achievement_collection_button.setFixedWidth(self.width()-27)
        self.achievement_collection_button.setFixedHeight(50)
        self.achievement_collection_button.move(10, 70)
        # --- Achievements Buttons
        # ------ Widget to contain scroll area; for resizing
        self.ab_scroll_area_container = QWidget(self)
        self.ab_scroll_area_container.resize(self.width()-10, 260)
        self.ab_scroll_area_container.move(10, 118)
        # ------ Scroll Area, to contain buttons
        self.ab_scroll_area = QScrollArea(self.ab_scroll_area_container)
        self.ab_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ab_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ab_scroll_area.setWidgetResizable(True)
        self.ab_scroll_area.resize(self.width()-10, 258)
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
        self.cab_layout.setContentsMargins(0, 10, 0, 0)
        self.cab_layout.setSpacing(18)
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
        self.create_new_page.ok_button.clicked.connect(self.create_new_achievement)
        self.create_new_button.clicked.connect(self.create_new_page.show)
        # --- Current Achievement Info Page
        self.current_achievement_info_page = CurrentAchievementInfoPage(self)
        self.current_achievement_info_page.hide()
        # --- Achievement Collection Page
        self.ach_collection_page = AchievementCollectionPage(self)
        self.ach_collection_page.hide()
        self.achievement_collection_button.clicked.connect(self.ach_collection_page.show)

        if True:
            self.create_new_achievement()

    def move(self, x, y):
        """ Move sub-main_menu_window as well."""
        super().move(x, y)
        self.ach_collection_page.move(x, y)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key.Key_Return:
            self.create_new_achievement()

    def sliding_page_in(self, page):
        sliding_page_anim = QPropertyAnimation(page, b"pos")
        sliding_page_anim.setEasingCurve(QEasingCurve.Type.OutCurve)
        sliding_page_anim.setDuration(300)
        sliding_page_anim.setEndValue(QPoint(0, 0))
        sliding_page_anim.start()

    def sliding_page_out(self, page):
        sliding_page_anim = QPropertyAnimation(page, b"pos")
        sliding_page_anim.setEasingCurve(QEasingCurve.Type.OutCurve)
        sliding_page_anim.setDuration(100)
        sliding_page_anim.setEndValue(QPoint(self.width(), 0))
        sliding_page_anim.start()

    def create_new_achievement(self):
        # Create achievement button
        title = self.create_new_page.title_entry.text()
        summary = self.create_new_page.summary_entry.text()
        description = self.create_new_page.description_entry.toPlainText()
        new_achievement_button = CurrentAchievementButton(title, summary, description)
        # Connect button to open info page
        def openCurrentAchievementInfoPage():
            self.current_achievement_info_page.setInfo(title, summary, description, new_achievement_button)
            self.current_achievement_info_page.show()
        new_achievement_button.clicked.connect(openCurrentAchievementInfoPage)
        # Connect complete button to completion
        def complete():
            # Add achievement button to collection page
            self.ach_collection_page.addAchievement(title, summary, description)
            # Remove achievement button from menu
            self.cab_layout.removeWidget(new_achievement_button)
            new_achievement_button.deleteLater()
            self.current_achievement_buttons.remove(new_achievement_button)
        new_achievement_button.complete_button.clicked.connect(complete)
        # Add to buttons
        self.current_achievement_buttons.append(new_achievement_button)
        # Insert button
        last_index = self.cab_layout.indexOf(self.create_new_button)
        self.cab_layout.insertWidget(last_index, new_achievement_button)
        self.create_new_page.clear()
        self.create_new_page.hide()

