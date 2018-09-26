#!/usr/bin/env python3

from typing import Tuple
from urllib.parse import quote

import pytesseract as pt
import requests
from PIL import ImageGrab
from PyQt5.QtCore import pyqtSignal, QObject, QPoint, QRect, QTimer, QThread

from config import JsConfig

import ueberfilter as uf


class ScumConfig(JsConfig):
    api_key = ""
    poll_period = 1
    selection = [[0, 0], [0, 0]]
    start_minimized = False

    def __init__(self, **js):
        super().__init__(**js)
        a, b = self.selection
        self.selection = QRect(QPoint(*a), QPoint(*b))
    
    def prepare_save(self):
        d = self.__dict__.copy()
        s = self.selection
        d['selection'] = [[s.left(), s.top()], [s.right(), s.bottom()]]
        return d


class OCR(QObject):
    textDetected = pyqtSignal(str)
    should = False

    selection = None

    def setSelection(self, sel: Tuple[int,int,int,int]):
        self.selection = sel

    def requestOcr(self):
        if self.should:
            return
        self.should = True
        QTimer.singleShot(0, self._performOcr)

    
    def _performOcr(self):
        self.should = False
        assert(self.selection is not None)
        print('> grabbing')
        img = ImageGrab.grab(self.selection)
        img = uf.beautify(img)
        # img.show()
        # img.save('ocr.png')
        print ('> ocring')
        s = pt.image_to_string(img)
        self.textDetected.emit(s)
        if self.should:
            QTimer.singleShot(0, self._performOcr)
        self.should = False

class Translator(QObject):
    translationDone = pyqtSignal(str)
    api_key = ""

    def setApi(self, api: str):
        self.api_key = api

    def performTranslation(self, original: str):
        self.translationDone.emit(original)
        return
        print('> translating', original)
        original = quote(original)
        if not self.api_key:
            return
        api = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
        url = f'{api}?key={self.api_key}&text={original}&lang=de-en'
        r = requests.post(url)
        if r.status_code != 200:
            raise RuntimeError(f'Yandex error:\n{r.content}')
        result = r.json()['text'][0]
        self.translationDone.emit(result)


class Uebersetzen(QObject):
    requestOcrSent = pyqtSignal()
    textDetected = pyqtSignal(str)
    textTranslated = pyqtSignal(str)

    ocr = OCR()
    tran = Translator()
    thr = QThread()

    config = None

    def __init__(self, config: ScumConfig):
        super().__init__()
        self.config = config
        self.timer = tm = QTimer(self)
        self._applyConfig()

        self.thr.start()

        self.ocr.moveToThread(self.thr)
        self.tran.moveToThread(self.thr)
        tm.timeout.connect(self.performOcr)

        self.requestOcrSent.connect(self.ocr.requestOcr)
        self.ocr.textDetected.connect(self.textDetected.emit)
        self.textDetected.connect(self.tran.performTranslation)
        self.tran.translationDone.connect(self.textTranslated.emit)


    def _applyConfig(self):
        c = self.config
        self.ocr.setSelection(c.selection.getCoords())
        self.tran.setApi(c.api_key)
        self.timer.setInterval(c.poll_period*1000)
    
    def performOcr(self):
        self.requestOcrSent.emit()
    
    def startOcr(self):
        self.timer.setInterval(self.config.poll_period*1000)
        self.timer.start()
    def stopOcr(self):
        self.timer.stop()
        

if __name__ == '__main__':
    def main():
        from PyQt5.QtCore import QCoreApplication
        from sys import argv
        app = QCoreApplication(argv)

        u = Uebersetzen(ScumConfig(**JsConfig.read_js('config.json')))
        # u.textDetected.connect(print)
        u.textTranslated.connect(print)
        u.textDetected.connect(lambda: QCoreApplication.quit()) # will quit immediately without lambda
        QTimer.singleShot(0, u.performOcr)

        app.exec_()
    main()