from PyQt5 import QtWidgets, QtGui, QtCore
import sys

class Overlay(QtWidgets.QWidget):
    grid_size = (8, 8)
    cell_size = None
    valid_swaps = None
    roi = None
    app = None
    close_flag = None

    def __init__(self, cell_size=90, roi=(135, 225)):
        super().__init__()
        self.init_ui()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | 
                            QtCore.Qt.WindowStaysOnTopHint | 
                            QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        self.cell_size = cell_size
        self.roi = roi
        self.show()

    def init_ui(self):
        close_button = QtWidgets.QPushButton("X", self)
        close_button.setGeometry(30, 30, 30, 30)
        close_button.clicked.connect(self.close)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addStretch()
        layout.addWidget(close_button)
        self.setLayout(layout)

    def close(self):
        self.close_flag = True
    
    def update_frame(self, valid_swaps):
        self.valid_swaps = valid_swaps

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setClipRect(event.rect())
        painter.setBrush(QtGui.QColor(0, 0, 0, 180))  # затемнение
        painter.drawRect(self.rect())

        # Прозрачные клетки
        for (r1, c1), (r2, c2) in self.valid_swaps:
            for r, c in [(r1, c1), (r2, c2)]:
                x = self.roi[1] + (c * self.cell_size)
                y = self.roi[0] + (r * self.cell_size)
                painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
                painter.fillRect(x, y, self.cell_size, self.cell_size, QtCore.Qt.transparent)
        # for r, c in self.valid_swaps:
        #     x = self.roi[0] + (c * self.cell_size)
        #     y = self.roi[1] + (r * self.cell_size)
        #     painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
        #     painter.fillRect(x, y, self.cell_size, self.cell_size, QtCore.Qt.transparent)
