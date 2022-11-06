from PyQt6.QtCore import QSize, QRect, Qt
from PyQt6.QtGui import QIcon, QFontMetricsF, QImage, QPainter, QBrush, QPixmap
from PyQt6.QtWidgets import QWidget, QToolButton, QLabel, QLineEdit, QPlainTextEdit, QPushButton, QFileDialog

from config import *
from RPGOverlay.data.objectiveinfo import AchievementInfo


class CreateAchievementPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        # Config
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # Property
        self.achievement_info = AchievementInfo()
        self._image = self.mask_image("images/trophy.png")
        self._title = ""
        self._summary = ""
        self._description = ""
        # Element
        # --- Background
        self.background = QWidget(self)
        self.background.setObjectName("panel")
        self.background.resize(self.size())
        # --- Back Button
        self.back_button = QPushButton("< Back", self)
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
        self.back_button.resize(50, 20)
        self.back_button.move(3, 3)
        self.back_button.clicked.connect(self.hide)
        # --- Create Achievement Label
        self.page_title = QLabel(self)
        self.page_title.setText("Create Achievement")
        self.page_title.setStyleSheet("""
            color: #adb1b8;
            font-size: 14pt;
        """)
        self.page_title.move(60, 4)
        # --- Image Upload Button
        self.image_upload_button = QToolButton(self.background)
        self.image_upload_button.setStyleSheet("""
            QToolButton {
                background-color: #424d61; 
                border: none;
                border-radius: 2px;
            }
            QToolButton::hover {
                background-color: #2b2b2b; 
            }
        """)
        self.image_upload_button.clicked.connect(self._getImage)
        self.image_upload_button.resize(QSize(60, 60))
        self.image_upload_button.setIcon(QIcon("images/image_upload_icon.png"))
        self.image_upload_button.setIconSize(QSize(26, 26))
        self.image_upload_button.move(10, 34)
        # --- Title Entry
        # ------ label
        self.title_label = QLabel("TITLE", self.background)
        self.title_label.setStyleSheet("""
            color: white;
            font-weight: bold;
        """)
        self.title_label.move(10, 104)
        # ------ entry
        self.title_entry = QLineEdit(self.background)
        self.title_entry.setStyleSheet("""
            background-color: #2b2b2b; 
            border: 0; 
            border-radius: 2px; 
            padding: 2px; 
            color: white;
        """)
        self.title_entry.textChanged.connect(       # record entry
            lambda: self._setTitle(self.title_entry.text()))
        self.title_entry.move(10, 124)
        self.title_entry.resize(222, 24)
        # --- Summary Entry
        # ------- label
        self.summary_label = QLabel("SUMMARY", self.background)
        self.summary_label.setStyleSheet("""
            color: white;
            font-weight: bold;
        """)
        self.summary_label.move(10, 154)
        # ------- entry
        self.summary_entry = QLineEdit(self.background)
        self.summary_entry.setStyleSheet("""
            background-color: #2b2b2b; 
            border: 0; border-radius: 2px; 
            padding: 2px; 
            color: white;
        """)
        self.summary_entry.textChanged.connect(     # record entry
            lambda: self._setSummary(self.summary_entry.text()))
        self.summary_entry.resize(222, 24)
        self.summary_entry.move(10, 174)
        # --- Description
        # ------ label
        self.description_label = QLabel("DESCRIPTION", self.background)
        self.description_label.setStyleSheet("""
            color: white;
            font-weight: bold;
        """)
        self.description_label.move(10, 204)
        # ------ entry
        self.description_entry = QPlainTextEdit(self.background)
        self.description_entry.setStyleSheet("""
            background-color: #2b2b2b; 
            border: 0; border-radius: 2px; 
            padding: 2px; 
            color: white;
        """)
        self.description_entry.setTabStopDistance(
            QFontMetricsF(self.description_entry.font()).horizontalAdvance(' ') * 4)
        self.description_entry.textChanged.connect(
            lambda: self._setDescription(self.description_entry.toPlainText()))
        self.description_entry.move(10, 224)
        self.description_entry.resize(226, 104)
        # Cancel Button
        self.cancel_button = QPushButton("Cancel", self.background)
        self.cancel_button.resize(66, 24)
        self.cancel_button.move(88, 339)
        self.cancel_button.setStyleSheet("""
            background-color: #636363;
            border-radius: 2px;
            color: white;
        """)
        self.cancel_button.clicked.connect(self.clear)
        self.cancel_button.clicked.connect(self.hide)
        # OK Button
        self.ok_button = QPushButton("OK", self.background)
        self.ok_button.resize(66, 24)
        self.ok_button.move(164, 339)
        self.ok_button.setStyleSheet("""
            background-color: #198cff;
            border-radius: 2px;
            color: white;
        """)
        self.ok_button.clicked.connect(
            lambda: self.achievement_info.setInfo(self._image, self._title, self._summary, self._description))

    def _getImage(self):
        filenames = QFileDialog.getOpenFileName(self, 'Open File', '', "Image file (*.png *.jpg *.jpeg *.bmp *.gif)")
        filename = next(f for f in filenames if not "")
        self._setImage(filename)

    def clear(self):
        self.achievement_info = AchievementInfo()
        self.title_entry.clear()
        self.summary_entry.clear()
        self.description_entry.clear()

    def _setTitle(self, new_title):
        self._title = new_title

    def _setSummary(self, new_summary):
        self._summary = new_summary

    def _setDescription(self, new_description):
        self._description = new_description

    def _setImage(self, new_image):
        try:
            self._image = self.mask_image(new_image)
            self.image_upload_button.setIcon(QIcon(self._image))  # reflect uploaded image
        except FileNotFoundError:
            self._image = self.mask_image(DEFAULT_IMAGE)
        self.image_upload_button.setIconSize(QSize(60, 60))

    @staticmethod
    def mask_image(imgpath):
        """
        Masking image to square. [46]
        return: pixmap of the squared image.
        """

        # Load image
        imgdata = open(imgpath, 'rb').read()
        image = QImage.fromData(imgdata)

        # convert image to 32-bit ARGB (adds an alpha
        # channel ie transparency factor)
        image.convertToFormat(QImage.Format.Format_ARGB32)

        # crop image to a square
        imgsize = min(image.width(), image.height())
        rect = QRect(
            int((image.width() - imgsize) / 2),
            int((image.height() - imgsize) / 2),
            imgsize,
            imgsize,
        )
        image = image.copy(rect)

        # Create the output image with the same dimension
        # and an alpha channel and make it completely transparent:
        out_img = QImage(imgsize, imgsize, QImage.Format.Format_ARGB32)
        out_img.fill(Qt.GlobalColor.transparent)

        # Create a texture brush and paint a *rounded
        # corners square with the original image onto
        # the output image:
        painter = QPainter(out_img)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Paint black background
        black_brush = QBrush(Qt.GlobalColor.black)
        painter.setBrush(black_brush)
        painter.drawRoundedRect(QRect(0, 0, imgsize, imgsize), 10, 10, Qt.SizeMode.RelativeSize)

        # Paint the output image
        brush = QBrush(image)
        painter.setBrush(brush)

        # Drawing rounded corner square [47]
        # Note the image size may vary so need to use RelativeSize mode [48]
        painter.drawRoundedRect(QRect(0, 0, imgsize, imgsize), 10, 10, Qt.SizeMode.RelativeSize)

        # Close painter event
        painter.end()

        # Last part is omitted from the reference [47]

        return QPixmap(out_img)
