from PyQt5.QtCore import QRect, QPoint
from typing import List, Tuple
import unittest

def cut(outer: QRect, inner: QRect) -> List[QRect]:
    assert(not inner.contains(outer))

    up = inner.top()
    left = inner.left()
    right = inner.right()


def rect_to_points(r: QRect) -> Tuple[QPoint, QPoint]:
    lt, rb = r.topLeft(), r.bottomRight()
    return lt, rb



class TestCut(unittest.TestCase):
    def test_inner(self):
        pass
        

if __name__ == '__main__':
    unittest.main()