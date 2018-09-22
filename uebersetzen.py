#!/usr/bin/env python3

from typing import Tuple
from urllib.parse import quote

import pytesseract as pt
import requests
from PIL import ImageGrab
from PyQt5.QtCore import pyqtSignal, QObject, QPoint, QRect, QTimer

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

    selection = None

    def setSelection(self, sel: Tuple[int,int,int,int]):
        self.selection = sel
    
    def performOcr(self):
        assert(self.selection is not None)
        print('> grabbing')
        img = ImageGrab.grab(self.selection)
        img = uf.beautify(img)
        # img.show()
        # img.save('ocr.png')
        print ('> ocring')
        s = pt.image_to_string(img)
        self.textDetected.emit(s)

class Translator(QObject):
    translationDone = pyqtSignal(str)
    api_key = ""

    def setApi(self, api: str):
        self.api_key = api

    def performTranslation(self, original: str):
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

    def __init__(self, config: ScumConfig):
        super().__init__()
        self.timer = tm = QTimer(self)
        tm.timeout.connect(self.performOcr)

        self.requestOcrSent.connect(self.ocr.performOcr)
        self.ocr.textDetected.connect(self.textDetected.emit)
        self.textDetected.connect(self.tran.performTranslation)
        self.tran.translationDone.connect(self.textTranslated.emit)

        self._applyConfig(config)

    def _applyConfig(self, c: ScumConfig):
        self.ocr.setSelection(c.selection.getCoords())
        self.tran.setApi(c.api_key)
        self.timer.setInterval(c.poll_period*1000)
    
    def performOcr(self):
        self.requestOcrSent.emit()
        

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