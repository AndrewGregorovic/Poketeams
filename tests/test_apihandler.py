import os
import sys
import unittest

import requests


sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/src")

from apihandler import APIHandler  # noqa: E402


class TestAPIHandlerClass(unittest.TestCase):
    def setUp(self):
        """Instantiate the api handler before each test"""
        self.test_api_handler = APIHandler()

    def test_api_url(self):
        """Test correct url is set on instantiation"""
        self.assertEqual(self.test_api_handler.api_url, "https://pokeapi.co/api/v2/", "The api url has been altered!")

    def test_get_single_pokemon(self):
        """Test APIHandler.get_pokemon() for retrieving a single pokemon"""
        test_response = self.test_api_handler.get_pokemon("nidoran-f")
        self.assertEqual(test_response.status_code, 200,
                         "The function didn't create the request url correctly returning a status code other than 200")
        self.assertIsInstance(test_response, requests.models.Response, "The function did not return a Response object!")

    def test_get_pokemon_with_query_string(self):
        """Test APIHandler.get_pokemon() for retrieving a list of pokemon"""
        test_response = self.test_api_handler.get_pokemon("", "?limit=107&offset=386")
        self.assertEqual(test_response.status_code, 200,
                         "The function didn't create the request url correctly returning a status code other than 200")
        self.assertIsInstance(test_response, requests.models.Response, "The function did not return a Response object!")

    def test_get_move(self):
        """Test APIHandler.get_move() for retrieving a move"""
        test_response = self.test_api_handler.get_move("scratch")
        self.assertEqual(test_response.status_code, 200,
                         "The function didn't create the request url correctly returning a status code other than 200")
        self.assertIsInstance(test_response, requests.models.Response, "The function did not return a Response object!")

    def test_get_ability(self):
        """Test APIHandler.get_ability() for retrieving an ability"""
        test_response = self.test_api_handler.get_ability("blaze")
        self.assertEqual(test_response.status_code, 200,
                         "The function didn't create the request url correctly returning a status code other than 200")
        self.assertIsInstance(test_response, requests.models.Response, "The function did not return a Response object!")
