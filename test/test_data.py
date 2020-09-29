import os
import sys
import unittest


sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                + "/src")

from data import Data


class TestDataClass(unittest.TestCase):
    def test_init_no_json_directory(self):
        pass

    def test_init_no_json_file(self):
        pass

    def test_init_invalid_json(self):
        pass

    def test_init_load_json(self):
        """Tests Data.convert_to_objects, Team.from_json, Pokemon.from_json,
        Move.from_json methods as all need to be called and function correctly
        in order to properly load the saved json data"""
        pass

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
