"""
    Objective: For RPGOverlay; To have system tray with window right below it.
    Current:
        - Icon tray & menu with utilities buttons and achievement menu
    To Do:
        - Button hover effect
"""

import sys
from app import Application


def main():
    # Create the App
    app = Application(sys.argv)

    app.exec()


if __name__ == "__main__":
    main()
