import os
import sys
import unittest


sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                + "/src")

from move import Move


class TestMoveClass(unittest.TestCase):
    def test_new_move_instance(self):
        pass