class Animation:
    def __init__(self):
        self.shrink_window = QPropertyAnimation()
        self.expend_window = QPropertyAnimation()

    def open_new_window(self, old, new):
        # Expand new window
        new.show()
        self.expend_window.setTargetObject(new)
        self.expend_window.setPropertyName(b'geometry')
        self.expend_window.setDuration(500)
        self.expend_window.setStartValue(QRect(new.x(), new.y(), 0, 0))
        self.expend_window.setEndValue(QRect(new.x() - new.width(), new.y(), new.width(), new.height()))
        self.expend_window.start()
        # Shrink old window
        """
        def shrink_old():
            self.shrink_window.setTargetObject(old)
            self.shrink_window.setPropertyName(b'geometry')
            self.shrink_window.setDuration(1000)
            self.shrink_window.setEndValue(QRect(old.x() + old.width, old.y(), 0, 0))
            self.shrink_window.start()
        """
        self.expend_window.finished.connect(old.hide)