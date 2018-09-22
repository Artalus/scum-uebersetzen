from PyQt5.QtCore import QPoint, QRect, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QMouseEvent, QPainter, QPen
from PyQt5.QtWidgets import (QApplication, QLabel, QPushButton,
                             QHBoxLayout, QWidget)

class TransWindow(QWidget):
    '''A transparent window to draw selection rect on
    '''
    selectionDone = pyqtSignal(QRect)

    start = QPoint(-1,-1)
    end = QPoint(-1,-1)

    def __init__(self, parent, selection=None, static=False):
        f = Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        super().__init__(parent, flags=f)
        self.static = static
        if selection:
            self.start = selection.topLeft()
            self.end = selection.bottomRight()

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.showMaximized()
        self.activateWindow()
        self.raise_()
        self.setGeometry(QApplication.desktop().availableGeometry())

    def mousePressEvent(self, ev :QMouseEvent):
        if (not self.static):
            self.start = ev.pos()
        else:
            self.close()

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255,0,0)))
        painter.fillRect(self.geometry(), QColor(0,255,0,10))
        painter.drawRect(QRect(self.start, self.end))
        # painter.fillRect(QRect(self.start, self.end), QColor(255,0,0,10))
        # painter.eraseRect(QRect(self.start, self.end))
        QWidget.paintEvent(self, ev)
    
    def mouseReleaseEvent(self, ev :QMouseEvent):
        if self.static: return

        r = QRect(self.start, ev.pos()).normalized()
        self.selectionDone.emit(r)
        self.close()
    
    def mouseMoveEvent(self, ev: QMouseEvent):
        if self.static: return

        self.end = ev.pos()
        self.repaint()
    
    def timerEvent(self, ev):
        self.close()
    

class Selector(QWidget):
    selectionChanged = pyqtSignal()

    def __init__(self, initial_selection=QRect(0, 0, 100, 100)):
        super().__init__()
        self.initUI()

        self._setRect(initial_selection, False)

    def initUI(self):
        btn = QPushButton('Select region')
        # btn.setGeometry(10, 20, 50, 10)
        btn.clicked.connect(self.init_selection)
        self.btn = btn

        self.lbl = QLabel()
        lay = QHBoxLayout()
        lay.addStretch(1)
        lay.addWidget(self.lbl)
        lay.addStretch(1)
        lay.addWidget(btn)
        self.setLayout(lay)

        btn = QPushButton('Show')
        btn.clicked.connect(self.showSelection)
        lay.addWidget(btn)

    def init_selection(self):
        w = TransWindow(self)
        w.show()
        w.selectionDone.connect(self._setRect)

    def showSelection(self):
        w = TransWindow(self, self.selection, True)
        w.startTimer(1000)

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
        # ex = TransWindow()
        ex = Selector()
        ex.show()
        # ex.selectionDone.connect(print)
        app.exec_()
    main()
