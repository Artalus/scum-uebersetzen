#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime as dt
from threading import Thread
from time import sleep

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import (QApplication, QMenu, QPushButton, QStyle, QSystemTrayIcon,
                             QTextBrowser, QVBoxLayout, QWidget)

from config import JsConfig
from selector import Selector


class ScumConfig(JsConfig):
    api_key = ""
    poll_period = 1
    selection = [[0, 0], [0, 0]]

    def __init__(self, **js):
        super().__init__(**js)
        a, b = self.selection
        self.selection = QRect(*a, *b)




class ChatLog(QTextBrowser):
    def __init__(self):
        super().__init__()
        self.setOpenExternalLinks(True)


class Tray(QSystemTrayIcon):
    def __init__(self, icon, params):
        super().__init__()
        self.setIcon(icon)
        self.params = params

        menu = QMenu(params)

        act = menu.addAction("Show window")
        act.triggered.connect(self.showWindow)

        act = menu.addAction("Exit")
        act.triggered.connect(self.params.exit)

        self.activated.connect(self.showWindow2)

        self.setContextMenu(menu)

    def showWindow(self):
        self.params.show()

    def showWindow2(self, ar: QSystemTrayIcon.ActivationReason):
        if ar == QSystemTrayIcon.Trigger:
            self.params.show()


class Writer(Thread):
    def __init__(self, cl: ChatLog):
        super().__init__()
        self.cl = cl

    def run(self):
        for _ in range(1, 11):
            ts = dt.now().strftime('%H:%M:%S')
            url = 'https://google.com'
            text = "razmolobzyr??"
            self.cl.append(f'[{ts}] <a href="{url}">{text}</a>')
            sleep(1)


class ParamsWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.exit = app.exit
        self.initUI()

    def initUI(self):
        self.selector = sel = Selector()
        sel.setGeometry(20, 40, 100, 50)
        

        lay = QVBoxLayout()
        lay.addWidget(sel)
        cl = ChatLog()
        lay.addWidget(cl)
        exitbutton = QPushButton('Exit')
        exitbutton.clicked.connect(self.exit)
        lay.addWidget(exitbutton)

        self.setLayout(lay)
        self.setGeometry(0, 0, 400, 400)
        self.setWindowTitle("SCÜM")
        t = Writer(cl)
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    def main():
        c = ScumConfig(**JsConfig.read_js('config.json'))

        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)

        ex = ParamsWindow(app)
        trayIcon = Tray(ex.style().standardIcon(
            QStyle.SP_DialogOpenButton), ex)

        trayIcon.show()
        ex.show()
        app.exec_()

    main()
