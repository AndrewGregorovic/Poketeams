import json
import os
import shutil
import sys
import unittest


project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/src"
sys.path.insert(1, project_path)

from data import Data  # noqa: E402
from move import Move  # noqa: E402
from pokemon import Pokemon  # noqa: E402
from team import Team  # noqa: E402


class TestDataClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            os.mkdir(project_path + "/json")
        except FileExistsError:
            pass

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(project_path + "/json")

    def tearDown(self):
        if os.path.exists(project_path + "/json"):
            with open(project_path + "/json/test_data.json", "w"):
                pass

    def test_init_no_json_directory(self):
        if os.path.exists(project_path + "/json"):
            shutil.rmtree(project_path + "/json")

        Data("test")
        self.assertTrue(os.path.exists(project_path + "/json"),
                        f"json directory not found in {project_path}!")

    def test_init_no_json_file(self):
        try:
            os.remove(project_path + "/json/test_data.json")
        except Exception:
            pass

        test_data_class = Data("test")
        self.assertEqual(test_data_class.team_data, [],
                         "team_data attribute has not been set to []!")

    def test_init_invalid_json(self):
        with open(project_path + "/json/test_data.json", "w") as f:
            f.write("invalid json data")

        test_data_class = Data("test")
        self.assertEqual(test_data_class.team_data, [],
                         "team_data attribute has not been set to []!")

    def test_init_load_json(self):
        """Tests Data.convert_to_objects, Team.from_json, Pokemon.from_json,
        Move.from_json methods as all need to be called and function correctly
        in order to properly load the saved json data"""

        default_move = ["None", "None", "None", "None", "None", "None", "None"]
        default_pokemon = ["None", "None", ("None",), "None", "None", {"None": "None"},
                           [], [Move(*default_move), Move(*default_move),
                                Move(*default_move), Move(*default_move)]]
        default_pokemon_list = [Pokemon(*default_pokemon),
                                Pokemon(*default_pokemon),
                                Pokemon(*default_pokemon),
                                Pokemon(*default_pokemon),
                                Pokemon(*default_pokemon),
                                Pokemon(*default_pokemon)]

        with open(project_path + "/json/test_data.json", "w") as f:
            f.write(json.dumps([Team("test1", default_pokemon_list),
                                Team("test2", default_pokemon_list)],
                               default=lambda o: o.__dict__))

        test_data_class = Data("test")
        self.assertIsInstance(test_data_class.team_data, list,
                              "team_data attribute is not a list!")
        self.assertEqual(len(test_data_class.team_data), 2,
                         "team_data attribute does not have 2 elements!")
        self.assertIsInstance(test_data_class.team_data[0], Team,
                              """first element of team_data is not a Team
                               object!""")
        self.assertEqual(test_data_class.team_data[0].name, "test1",
                         """first team_data element does not have a name
                          attribute with value 'test1'!""")
        self.assertIsInstance(test_data_class.team_data[0].pokemon_list[0],
                              Pokemon, """first element in test1 Team's
                              pokemon_list is not a Pokemon object""")
        self.assertIsInstance(test_data_class.team_data[0].pokemon_list[0].
                              move_set[0], Move, """first element in Pokemon
                               object's move_set is not a Move object!""")

    def test_menu_options_disabled(self):
        test_data_class = Data("test")
        test_data_class.team_data = []
        self.assertIsInstance(test_data_class.get_main_menu_options()[1],
                              dict, "Load a saved team option is not a dict!")
        self.assertIsInstance(test_data_class.get_main_menu_options()[2],
                              dict, """Delete a saved team option is not a
                               dict!""")

    def test_menu_options_enabled(self):
        test_data_class = Data("test")
        test_data_class.team_data = [Team("menu_options_enabled?",
                                     test_data_class.default_pokemon_list)]
        self.assertIsInstance(test_data_class.get_main_menu_options()[1],
                              str, "Load a saved team option is not a str!")
        self.assertIsInstance(test_data_class.get_main_menu_options()[2],
                              str, "Delete a saved team option is not a str!")

    # def test_new_team(self):
    #     test_data_class = Data("test")
    #     test_data_class.new_team()  # need to try and mock prompt input
    #     self.assertEqual(test_data_class.team_data[0].name, "test team name")
    #     self.assertIsInstance(test_data_class.current_team, Team)
    #     self.assertEqual(test_data_class.current_team,
    #                      test_data_class.team_data[0])

    # def test_current_team_after_load(self):
    #     test_data_class = Data("test")
    #     test_data_class.team_data = [Team("test team 1",
    #                                  test_data_class.default_pokemon_list),
    #                                  Team("test team 2",
    #                                  test_data_class.default_pokemon_list)]
    #     test_data_class.load_saved_team()  # need to mock select_saved_team()
    #     self.assertEqual(test_data_class.team_data[1],
    #                      test_data_class.current_team)

    # def test_delete_team_from_team_data(self):
    #     test_data_class = Data("test")
    #     test_data_class.team_data = [Team("test team 1",
    #                                  test_data_class.default_pokemon_list),
    #                                  Team("test team 2",
    #                                  test_data_class.default_pokemon_list)]
    #     test_data_class.current_team = test_data_class.team_data[0]
    #     test_data_class.delete_saved_team()  # need to mock select_saved_team()
    #     self.assertEqual(len(test_data_class.team_data), 1)
    #     self.assertEqual(test_data_class.team_data[0].name, "test team 2")
    #     self.assertIsNone(test_data_class.current_team)

    def test_save_no_team_data(self):
        test_data_class = Data("test")
        test_data_class.team_data = []
        test_data_class.save_all_teams()
        with open(project_path + "/json/test_data.json", "r") as f:
            self.assertEqual(f.read(), "", """json file is not empty even
                             though there's no team data!""")

    # def test_save_team_data(self):
    #     pass
    #     test_dumped_data =  # get this after finalising the pokemon/move data
    #     test_data_class = Data("test")
    #     test_data_class.team_data = [Team("test team",
    #                                  test_data_class.default_pokemon_list)]
    #     test_data_class.save_all_teams()
    #     with open(os.path.dirname(os.path.abspath(__file__))
    #               + "/json/team_data.json", "r") as f:
    #         saved_data = json.loads(f.read())
    #     self.assertEqual(saved_data, test_dumped_data)
