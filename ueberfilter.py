from PIL import Image, ImageGrab
import numpy as np
import numpy
import cv2
from PIL.ImageEnhance import *
from PIL.ImageFilter import *

def pil_to_cv2(img: Image):
    return cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)

def cv2_to_pil(img) -> Image:
    return Image.fromarray(img)

def beautify(img: Image) -> Image:
    # # img.show()
    # img2 = Color(img).enhance(0)
    # # img2.show()
    # img3 = Contrast(img2).enhance(3)
    # img3.show()
    # img4 = Brightness(img3).enhance(0.5)
    # img4.show()
    # img5 = Contrast(img4).enhance(2)
    # img5.show()
    # img6 = img5.filter(Kernel((3,3), [.2]*9))
    # img6.show()
    # return None
    gray = pil_to_cv2(img)

    # gray = cv2.equalizeHist(gray)
    # cv2.imshow('eq', gray)
    
    gray = cv2.resize(gray, None, fx=2,fy=2, interpolation=cv2.INTER_LINEAR)
    cv2.imshow('scaled', gray)

    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    cv2.imshow('origin', gray)
    # g2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray = cv2.threshold(gray, 100, 255, cv2.THRESH_TOZERO)[1]
    cv2.imshow('thresh_zero', gray)
    # gray3 = cv2.adaptiveThreshold(gray2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    return cv2_to_pil(cv2.bitwise_not(gray))


def main():
    # img = ImageGrab.grab((20, 640, 700, 800))
    img = Image.open('C:\\Users\\Artalus\\Pictures\\ice_video_20180922-131545.webm_snapshot_00.09_[2018.09.22_23.24.29].png')
    beautify(img)

if __name__ == '__main__':
    main()
    cv2.waitKey()