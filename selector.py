from PyQt5.QtCore import QPoint, QRect, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QMouseEvent, QPainter, QPalette, QPen
from PyQt5.QtWidgets import (QApplication, QLabel, QPushButton,
                             QHBoxLayout, QWidget)

class TransWindow(QWidget):
    '''A transparent window to draw selection rect on
    '''
    selectionDone = pyqtSignal(QRect)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.start = QPoint(0,0)
        self.end = QPoint(0,0)

        # palette = QPalette()
        # palette.setColor(QPalette.Base, Qt.transparent)
        # self.setPalette(palette)

        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setStyleSheet("background:transparent;")

        self.showMaximized()
        self.activateWindow()
        self.raise_()
        self.setWindowFlags(0 \
                            # | Qt.CustomizeWindowHint
                            # | Qt.Window \
                            | Qt.WindowStaysOnTopHint  \
                            # | Qt.X11BypassWindowManagerHint \
                            | Qt.FramelessWindowHint )

        self.setGeometry(QApplication.desktop().availableGeometry())
        # self.setWindowOpacity(0.5)

    def mousePressEvent(self, ev :QMouseEvent):
        self.start = ev.pos()

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255,0,0)))
        painter.fillRect(self.geometry(), QColor(0,255,0,10))
        painter.drawRect(QRect(self.start, self.end))
        # painter.fillRect(QRect(self.start, self.end), QColor(255,0,0,10))
        # painter.eraseRect(QRect(self.start, self.end))
        QWidget.paintEvent(self, ev)
    
    def mouseReleaseEvent(self, ev :QMouseEvent):
        r = QRect(self.start, ev.pos()).normalized()
        self.selectionDone.emit(r)
        self.close()
    
    def mouseMoveEvent(self, ev: QMouseEvent):
        self.end = ev.pos()
        self.repaint()
    

class Selector(QWidget):
    selectionChanged = pyqtSignal()

    def __init__(self, initial_selection=QRect(0, 0, 100, 100)):
        super().__init__()
        self.initUI()

        self._setRect(initial_selection, False)

    def initUI(self):
        btn = QPushButton('Select region')
        btn.setGeometry(10, 20, 50, 10)
        btn.clicked.connect(self.init_selection)
        self.btn = btn

        self.lbl = QLabel()
        lay = QHBoxLayout()
        lay.addStretch(1)
        lay.addWidget(self.lbl)
        lay.addStretch(1)
        lay.addWidget(btn)
        self.setLayout(lay)

    def init_selection(self):
        w = TransWindow(self)
        w.show()
        w.selectionDone.connect(self._setRect)

    def _setRect(self, selection: QRect, do_emit=True):
        self.selection = selection
        l,t,r,b = selection.getCoords()
        self.lbl.setText(f'From ({l},{t}) to ({r},{b})')
        if do_emit:
            self.selectionChanged.emit()


if __name__ == '__main__':
    def main():
        import sys
        app = QApplication(sys.argv)
        ex = TransWindow()
        ex.show()
        ex.selectionDone.connect(print)
        app.exec_()
    main()
