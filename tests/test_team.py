import os
import sys
import unittest


sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/src")

# from team import Team  # noqa: E402


class TestTeamClass(unittest.TestCase):
    def setUp(self):
        pass

    def test_new_team_instance(self):
        pass

    def test_save_new_team_data(self):
        pass

    def test_save_updated_team_data(self):
        pass
