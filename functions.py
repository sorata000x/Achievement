import os

from PyQt6.QtGui import QFontDatabase, QFont


def getFont(filename):
    font_id = QFontDatabase.addApplicationFont(f"{os.path.dirname(__file__)}/fonts/{filename}")
    try:
        if font_id > -1:
            font_name = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_name, 34)
            return font
        else:
            raise Exception()
    except Exception:
        print("Font file not found.")
        exit()
