#!/usr/bin/env python3

import PIL
from PIL import ImageGrab

import pytesseract as pt

from datetime import datetime as dt
from time import sleep

from PyQt5.QtCore import pyqtSignal, QObject, QPoint, QRect, QTimer
from config import JsConfig


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
