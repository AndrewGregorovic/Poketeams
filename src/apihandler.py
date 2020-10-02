import requests


class APIHandler():
    """
    A class to control the api requests made by the application

    Attributes:
    api_url: str
        The url of the api

    Methods:
    get_pokemon(self, name: str, query_string: str = "")
        Constructs the full request url for a pokemon and returns the response

    get_move(self, name: str)
        Constructs the full request url for a move and returns the response

    get_ability(self, name: str)
        Constructs the full request url for an ability and returns the response
    """

    def __init__(self) -> None:
        """
        Sets the required attributes for the APIHandler object
        """

        self.api_url: str = "https://pokeapi.co/api/v2/"

    def get_pokemon(self, name: str, query_string: str = "") -> requests.models.Response:
        """
        Constructs the full request url for a pokemon and returns the response

        Parameters:
        name: str
            String of the pokemon's name or pokedex number

        query_string: str, optional, default = ""
            Additional data to add to the request url, used for requesting the pokemon lists for each generation

        Returns:
        Response object from the api call
        """

        request_url = self.api_url + "pokemon/" + name + query_string
        return requests.get(request_url)

    def get_move(self, name: str) -> requests.models.Response:
        """
        Constructs the full request url for a move and returns the response

        Parameters:
        name: str
            String of the move's name, will also accept the move's id number but less likely to be given

        Returns:
        Response object from the api call
        """

        request_url = self.api_url + "move/" + name
        return requests.get(request_url)

    def get_ability(self, name: str) -> requests.models.Response:
        """
        Constructs the full request url for an ability and returns the response

        Parameters:
        name: str
            String of the ability's name, will also accept the ability's id number but less likely to be given

        Returns:
        Response object from the api call
        """

        request_url = self.api_url + "ability/" + name
        return requests.get(request_url)
