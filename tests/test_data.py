import json
import os
import shutil
import sys
import unittest


project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) \
               + "/src"
sys.path.insert(1, project_path)

from data import Data
from move import Move
from pokemon import Pokemon
from team import Team


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
            with open(project_path + "/json/test_data.json", "w") as f:
                    pass

    def test_init_no_json_directory(self):
        if os.path.exists(project_path + "/json"):
            shutil.rmtree(project_path + "/json")

        test_data_class = Data("test")
        self.assertTrue(os.path.exists(project_path + "/json"))

    def test_init_no_json_file(self):
        try:
            os.remove(project_path + "/json/test_data.json")
        except Exception:
            pass

        test_data_class = Data("test")
        self.assertEqual(test_data_class.team_data, [])

    def test_init_invalid_json(self):
        with open(project_path + "/json/test_data.json", "w") as f:
            f.write("invalid json data")
        
        test_data_class = Data("test")
        self.assertEqual(test_data_class.team_data, [])

    def test_init_load_json(self):
        """Tests Data.convert_to_objects, Team.from_json, Pokemon.from_json,
        Move.from_json methods as all need to be called and function correctly
        in order to properly load the saved json data"""

        default_move = ["None", "None", "None", "None", "None", "None", "None"]
        default_pokemon = ["None", "None", "None", "None", "None", "None", "None",
                           [Move(*default_move), Move(*default_move),
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
        self.assertIsInstance(test_data_class.team_data, list)
        self.assertEqual(len(test_data_class.team_data), 2)
        self.assertIsInstance(test_data_class.team_data[0], Team)
        self.assertEqual(test_data_class.team_data[0].name, "test1")
        self.assertIsInstance(test_data_class.team_data[0].pokemon_list[0],
                              Pokemon)
        self.assertIsInstance(test_data_class.team_data[0].pokemon_list[0]. \
                              move_set[0], Move)

    def test_menu_options_disabled(self):
        pass

    def test_menu_options_enabled(self):
        pass

    def test_new_team_name(self):
        pass

    def test_current_team_after_new(self):
        pass

    def test_team_choices(self):
        pass

    def test_current_team_after_load(self):
        pass

    def test_delete_team_from_team_data(self):
        pass

    def test_current_team_after_delete(self):
        pass

    def test_save_no_team_data(self):
        pass

    def test_save_team_data(self):
        pass
