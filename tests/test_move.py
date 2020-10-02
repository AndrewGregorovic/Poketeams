import os
import sys
import unittest


sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/src")

from move import Move  # noqa: E402


class TestMoveClass(unittest.TestCase):

    def setUp(self):
        """Set defaults for creating test Move objects"""
        self.default_move = ["None", 0, 0, 0, "None", 0, "None"]

    def test_init(self):
        """Test instantiation"""
        try:
            test_move = Move(*self.default_move)
            test_move.name
            test_move.accuracy
            test_move.power
            test_move.pp
            test_move.type
            test_move.effect_chance
            test_move.effect
        except Exception as e:
            self.assertTrue(False, e)

    def test_get_move_options(self):
        """Test Move.get_move_options()"""
        test_move = Move(*self.default_move)
        test_options = test_move.get_move_options("online")
        self.assertIsInstance(test_options, list, "test options are not being returned as a list of options!")
        self.assertEqual(len(test_options), 2, "the number of options being returned is not equal to 2!")

        test_options = test_move.get_move_options("offline")
        self.assertIsInstance(test_options, list, "test options are not being returned as a list of options!")
        self.assertEqual(len(test_options), 1, "the number of options being returned is not equal to 1!")
