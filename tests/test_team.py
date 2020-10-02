import os
import sys
import unittest


sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/src")

from move import Move  # noqa: E402
from pokemon import Pokemon  # noqa: E402
from team import Team  # noqa: E402


class TestTeamClass(unittest.TestCase):

    def setUp(self):
        """Set defaults for creating test Team objects"""
        self.default_move = ["None", 0, 0, 0, "None", 0, "None"]
        self.default_pokemon = [0, "None", ("None",), 0, 0, {"None": "None"}, [],
                                [Move(*self.default_move), Move(*self.default_move), Move(*self.default_move), Move(*self.default_move)]]
        self.default_pokemon_list = [Pokemon(*self.default_pokemon), Pokemon(*self.default_pokemon), Pokemon(*self.default_pokemon),
                                     Pokemon(*self.default_pokemon), Pokemon(*self.default_pokemon), Pokemon(*self.default_pokemon)]

    def test_init(self):
        """Test instantiation"""
        try:
            test_team = Team("test team", self.default_pokemon_list)
            test_team.name
            test_team.pokemon_list
        except Exception as e:
            self.assertTrue(False, e)

    def test_get_team_options(self):
        """Test Team.get_team_options()"""
        test_team = Team("test options", self.default_pokemon_list)

        test_options = test_team.get_team_menu_options("online")
        self.assertEqual(test_options[0], "Edit team", "The first option does not have the name Edit team!")

        test_options = test_team.get_team_menu_options("offline")
        self.assertIsInstance(test_options[0], dict, "The first option is not correctly disabled for offline mode with an empty team!")

        default_pokemon = [0, "Test pokemon", ("None",), 0, 0, {"None": "None"}, [],
                           [Move(*self.default_move), Move(*self.default_move), Move(*self.default_move), Move(*self.default_move)]]
        pokemon_list = [Pokemon(*default_pokemon), Pokemon(*self.default_pokemon), Pokemon(*self.default_pokemon),
                        Pokemon(*self.default_pokemon), Pokemon(*self.default_pokemon), Pokemon(*self.default_pokemon)]
        test_team = Team("test not empty team", pokemon_list)
        test_options = test_team.get_team_menu_options("offline")
        self.assertEqual(test_options[0], "View Pokémon", "The first option is not correctly named for offline mode!")

    def test_team_save(self):
        """Test Team.team_save()"""
        test_team_data = [Team("test team 1", self.default_pokemon_list),
                          Team("test team 2", self.default_pokemon_list)]
        default_pokemon = [0, "Test pokemon", ("None",), 0, 0, {"None": "None"}, [],
                           [Move(*self.default_move), Move(*self.default_move), Move(*self.default_move), Move(*self.default_move)]]
        pokemon_list = [Pokemon(*default_pokemon), Pokemon(*self.default_pokemon), Pokemon(*self.default_pokemon),
                        Pokemon(*self.default_pokemon), Pokemon(*self.default_pokemon), Pokemon(*self.default_pokemon)]
        test_team = Team("test team 2", pokemon_list)
        updated_team_data = test_team.team_save(test_team_data)
        self.assertEqual(test_team.name, updated_team_data[1].name, "test team 2 does not have the same name as the team at test_team_data[1]!")
        self.assertEqual(test_team.pokemon_list[0].name, updated_team_data[1].pokemon_list[0].name, "test team 2 not correctly updated with new team data!")

        test_team = Team("new test team", pokemon_list)
        new_team_data = test_team.team_save(test_team_data)
        self.assertEqual(len(new_team_data), 3, "new test team has not been added as the 3rd element of test_team_data!")
        self.assertEqual(test_team, new_team_data[2], "new test team is not the 3rd element of test_team_data but should've been appended!")
