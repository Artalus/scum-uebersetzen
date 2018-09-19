#!/usr/bin/env python3

import PIL
from PIL import ImageGrab

import pytesseract as pt

from datetime import datetime as dt
from time import sleep

for i in range(10):
    start = dt.now()
    img = ImageGrab.grab((100,200,600,800))
    mid = dt.now()
    img.save("saved%d.png" % i)
    end = dt.now()
    print('grab: {}, save: {}'.format(mid-start, end-mid))
    sleep(1)