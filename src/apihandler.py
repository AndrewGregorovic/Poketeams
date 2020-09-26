import requests
import json

class APIHandler():
    api_url = "https://pokeapi.co/api/v2/"

    def get_pokemon(self, name, query_string = ""):
        request_url = self.api_url + "pokemon/" + name + query_string
        return json.loads(requests.get(request_url).text)

    def get_move(self, name):
        request_url = self.api_url + "move/" + name
        return json.loads(requests.get(request_url).text)