import os
import sys
import unittest


sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/src")

# from pokemon import Pokemon  # noqa: E402


class TestPokemonClass(unittest.TestCase):

    def setUp(self):
        pass

    def test_new_pokemon_instance(self):
        pass

    def test_pokemon_move_option_disabled(self):
        pass

    def test_pokemon_move_option_enabled(self):
        pass
