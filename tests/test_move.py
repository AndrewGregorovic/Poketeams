import os
import sys
import unittest


sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/src")

# from move import Move  # noqa: E402


class TestMoveClass(unittest.TestCase):

    def setUp(self):
        pass

    def test_new_move_instance(self):
        pass
