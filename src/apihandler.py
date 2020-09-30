import json

import requests


class APIHandler():
    api_url = "https://pokeapi.co/api/v2/"

    def get_pokemon(self, name, query_string=""):
        request_url = self.api_url + "pokemon/" + name + query_string
        return requests.get(request_url)

    def get_move(self, name):
        request_url = self.api_url + "move/" + name
        return requests.get(request_url)

    def get_ability(self, name):
        request_url = self.api_url + "ability/" + name
        return requests.get(request_url)
