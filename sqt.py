#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime as dt
from threading import Thread
from time import sleep

from PyQt5.QtCore import QPoint, QRect, pyqtSignal, Qt
from PyQt5.QtWidgets import (QApplication, QMenu, QPushButton, QStyle, QSystemTrayIcon, QLabel,
                             QTextBrowser, QVBoxLayout, QCheckBox, QHBoxLayout, QWidget)

from uebersetzen import ScumConfig

from config import JsConfig
from selector import Selector





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
        act.triggered.connect(QApplication.exit)

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


from uebersetzen import Uebersetzen

class ParamsWindow(QWidget):
    triggerConfigSave = pyqtSignal()

    def __init__(self, configname: str):
        super().__init__()
        self.configname = configname
        self.config = ScumConfig(**JsConfig.read_js(configname))
        self.ub = Uebersetzen(self.config)
        self.ub.textTranslated.connect(self.write)

        self.initUI()

        self.triggerConfigSave.connect(self.saveConfig)

    def initUI(self):
        self.selector = sel = Selector(self.config.selection)
        sel.selectionChanged.connect(self.triggerConfigSave.emit)
        sel.setGeometry(20, 40, 100, 50)
        
        hb = QHBoxLayout()
        ocr = QPushButton('Über!')
        ocr.clicked.connect(self.ueber)
        hb.addWidget(ocr)
        hb.addWidget(sel)

        lay = QVBoxLayout()
        lay.addLayout(hb)

        self.chatlog = cl = ChatLog()
        lay.addWidget(cl)

        hb = QHBoxLayout()
        self.minimized_checkbox = sm = QCheckBox('Start minimized')
        sm.setTristate(False)
        sm.setChecked(self.config.start_minimized)
        sm.stateChanged.connect(self.triggerConfigSave.emit)
        hb.addWidget(sm)

        hb.addStretch(1)
        exitbutton = QPushButton('Exit')
        exitbutton.clicked.connect(QApplication.exit)
        hb.addWidget(exitbutton)
        lay.addLayout(hb)

        license_lbl = QLabel('Translation performed via <a href="https://translate.yandex.ru">"Yandex.Translate"</a> service')
        license_lbl.setOpenExternalLinks(True)
        lay.addWidget(license_lbl)

        self.setLayout(lay)
        self.setGeometry(0, 0, 400, 400)
        self.setWindowTitle("SCÜM")
        # t = Writer(cl)
        # t.setDaemon(True)
        # t.start()

        if not self.config.start_minimized:
            self.show()

    def saveConfig(self):
        c = self.config

        c.selection = self.selector.selection
        c.start_minimized = self.minimized_checkbox.checkState() == Qt.Checked

        c.save_to_file(self.configname)
        self.ub._applyConfig(c)

    def ueber(self):
        self.ub.performOcr()

    def write(self, text: str):
        self.chatlog.setText(text)


if __name__ == '__main__':
    def main():

        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)

        ex = ParamsWindow('config.json')
        trayIcon = Tray(ex.style().standardIcon(
            QStyle.SP_DialogOpenButton), ex)

        trayIcon.show()
        app.exec_()

    main()
