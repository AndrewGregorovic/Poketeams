import os
import sys
import unittest


sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/src")

from move import Move  # noqa: E402
from pokemon import Pokemon  # noqa: E402


class TestPokemonClass(unittest.TestCase):

    def setUp(self):
        """Set defaults for creating test Team objects"""
        self.default_move = ["None", 0, 0, 0, "None", 0, "None"]
        self.default_pokemon = [0, "None", ("None",), 0, 0, {"None": "None"}, [],
                                [Move(*self.default_move), Move(*self.default_move),
                                 Move(*self.default_move), Move(*self.default_move)]]

    def test_init(self):
        """Test instantiation"""
        try:
            test_pokemon = Pokemon(*self.default_pokemon)
            test_pokemon.id
            test_pokemon.name
            test_pokemon.types
            test_pokemon.weight
            test_pokemon.height
            test_pokemon.abilities
            test_pokemon.move_list
            test_pokemon.move_set
        except Exception as e:
            self.assertTrue(False, e)

    def test_get_pokemon_options(self):
        """Test Pokemon.get_pokemon_options()"""
        test_pokemon = Pokemon(*self.default_pokemon)
        test_options = test_pokemon.get_pokemon_options("online")
        self.assertIsInstance(test_options[1], dict, "Change moves option isn't disabled on an empty pokemon slot!")

        test_options = test_pokemon.get_pokemon_options("offline")
        self.assertIsInstance(test_options[0], dict, "View moves option isn't disabled on an empty pokemon slot when offline!")

        default_pokemon = [0, "Test options pokemon", ("None",), 0, 0, {"None": "None"}, [],
                           [Move(*self.default_move), Move(*self.default_move),
                            Move(*self.default_move), Move(*self.default_move)]]
        test_pokemon = Pokemon(*default_pokemon)
        test_options = test_pokemon.get_pokemon_options("online")
        self.assertEqual(test_options[1], "Change moves", "Change moves option isn't enabled on an occupied pokemon slot!")

        test_options = test_pokemon.get_pokemon_options("offline")
        self.assertEqual(test_options[0], "View moves", "View moves option isn't correctly named or enabled on an empty pokemon slot when offline!")
