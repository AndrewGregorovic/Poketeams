import requests


class APIHandler():

    def __init__(self) -> None:
        self.api_url: str = "https://pokeapi.co/api/v2/"

    def get_pokemon(self, name: str, query_string: str = "") -> requests.models.Response:
        """
        Construct the request url for the api call
        name, can either be the pokemons name or its pokedex number as a string
        query_string (optional), is used for requesting the pokemon lists for each generation
        """
        request_url = self.api_url + "pokemon/" + name + query_string
        return requests.get(request_url)

    def get_move(self, name: str) -> requests.models.Response:
        request_url = self.api_url + "move/" + name
        return requests.get(request_url)

    def get_ability(self, name: str) -> requests.models.Response:
        request_url = self.api_url + "ability/" + name
        return requests.get(request_url)
