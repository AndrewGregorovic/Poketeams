import json

from PyInquirer import prompt  # type: ignore
import requests

from apihandler import APIHandler


class Move():
    """
    A class to represent a pokemon move

    Attributes:
    name: str
        Name of the move
    accuracy: int
        Accuracy of the move in percent
    power: int
        The power of the move
    pp: int
        The power points of the move
    type: str
        The type that the move belongs to
    effect_chance: int
        The percent chance of an additional effect caused by the move
    effect: str
        Description of what the move does

    Methods:
    from_json(cls, data: dict)
        Creates a Move object from a json dictionary

    from_response(cls, response: requests.models.Response)
        Creates a Move object from a Response object

    view_move(self, team_name: str, pokemon_choice: str, pokemon_name: str)
        Displays the Move object's information

    get_move_options(mode: str)
        Gets the options to use in Move.move_menu()

    move_menu(self, mode: str)
        Displays the menu for the Move screen

    view_move_list(pokemon_name: str, pokemon_move_list: list, pokemon_move_set: list)
        Displays the list of moves that can be saved to the currently selected move slot

    select_move(api_handler: APIHandler)
        Displays the input field for the user to select and search for a move

    confirm_move()
        Get confirmation to add the move to the currently selected move slot
    """

    def __init__(self, name: str, accuracy: int, power: int, pp: int, type: str, effect_chance: int, effect: str) -> None:
        """
        Sets the required attributes for the Move object

        Parameters:
        name: str
            Name of the move
        accuracy: int
            Accuracy of the move in percent
        power: int
            The power of the move
        pp: int
            The power points of the move
        type: str
            The type that the move belongs to
        effect_chance: int
            The percent chance of an additional effect caused by the move
        effect: str
            Description of what the move does
        """

        self.name: str = name
        self.accuracy: int = accuracy
        self.power: int = power
        self.pp: int = pp
        self.type: str = type
        self.effect_chance: int = effect_chance
        self.effect: str = effect

    @classmethod
    def from_json(cls, data: dict) -> "Move":
        """
        Creates a Move object from a json dictionary

        Parameters:
        data: dict
            Dictionary containing attribute, value pairs from the applications saved json data

        Returns:
        Move object
        """

        return cls(**data)

    @classmethod
    def from_response(cls, response: requests.models.Response) -> "Move":
        """
        Creates a Move object from a Response object

        Parameters:
        response: requests.models.Response
            Response object from APIHandler.get_move()

        Returns:
        Move object
        """

        api_data: dict = json.loads(response.text)
        name: str = api_data["name"].capitalize()

        if api_data["accuracy"] is None:
            accuracy: int = 0
        else:
            accuracy = api_data["accuracy"]

        if api_data["power"] is None:
            power: int = 0
        else:
            power = api_data["power"]

        pp: int = api_data["pp"]

        type: str = api_data["type"]["name"].capitalize()

        if api_data["effect_chance"] is None:
            effect_chance: int = 0
        else:
            effect_chance = api_data["effect_chance"]

        for effect_entry in api_data["effect_entries"]:
            if effect_entry["language"]["name"] == "en":
                effect: str = effect_entry["effect"].replace("\n", " ").replace("  ", " ")

        return cls(name, accuracy, power, pp, type, effect_chance, effect)

    def view_move(self, team_name: str, pokemon_choice: str, pokemon_name: str) -> None:
        """
        Displays the Move object's information

        Parameters:
        team_name: str
            The name attribute of the currently selected Team
        pokemon_choice: str
            The move slot number of the currently selected Pokemon
        pokemon_name: str
            The name attribute of the currently selected Pokemon

        Returns:
        None
        """

        print(f"\n\u001b[1m\u001b[4mTeam\u001b[0m: \u001b[7m {team_name} \u001b[0m")
        print(f"\u001b[1m\u001b[4mPokémon\u001b[0m: \u001b[4m{pokemon_name}\u001b[0m")
        print(f"\n\u001b[4mMove Slot #{int(pokemon_choice)}\u001b[0m\n\n")
        print(f"\u001b[1mName\u001b[0m: {self.name}\n")
        print(f"\u001b[1mPower\u001b[0m: {self.power}")
        print(f"\u001b[1mAccuracy\u001b[0m: {self.accuracy}" + "%")
        print(f"\u001b[1mPP\u001b[0m: {self.pp}\n")
        print(f"\u001b[1mType\u001b[0m: {self.type}")
        print("")
        print(f"\u001b[1mEffect Chance\u001b[0m: {self.effect_chance}" + "%")
        print("\n\u001b[1mEffect\u001b[0m:")
        print(f"    {self.effect}")
        print("\n")

    @staticmethod
    def get_move_options(mode: str) -> list:
        """
        Gets the options to use in Move.move_menu()

        Parameters:
        mode: str
            The currently running mode of the application

        Returns:
        List of menu options to display in Move.move_menu()
        """

        options: list = [
            "Change move",
            "Back to Pokémon view"
        ]

        if mode == "online":
            return options
        else:
            return options[1:]

    def move_menu(self, mode: str) -> str:
        """
        Displays the menu for the Move screen

        Parameters:
        mode: str
            The currently running mode of the application

        Returns:
        String of the user's input from the PyInquirer prompt
        """

        move_options: list = [
            {
                "type": "list",
                "name": "move_menu",
                "message": "What would you like to do with this move slot?",
                "choices": self.get_move_options(mode)
            }
        ]

        return prompt(move_options)["move_menu"]

    @staticmethod
    def view_move_list(pokemon_name: str, pokemon_move_list: list, pokemon_move_set: list) -> None:
        """
        Displays the list of moves that can be saved to the currently selected move slot

        Parameters:
        pokemon_name: str
            The name attribute of the currently selected Pokemon
        pokemon_move_list: list
            The move_list attribute of the currently selected Pokemon
        pokemon_move_set: list
            The move_set attribute of the currently selected Pokemon

        Returns:
        None
        """

        learnt_moves: list = [move.name for move in pokemon_move_set]
        unlearnt_moves: list = []
        for move in pokemon_move_list:
            if move not in learnt_moves:
                unlearnt_moves.append(f" {move} ")

        while len(unlearnt_moves) % 4 != 0:
            unlearnt_moves.append("")

        print(f"\u001b[1m\u001b[4m{pokemon_name} can learn the following moves\u001b[0m:\n")
        for a, b, c, d in zip(unlearnt_moves[::4], unlearnt_moves[1::4], unlearnt_moves[2::4], unlearnt_moves[3::4]):
            print("{:<29}{:<29}{:<29}{:<29}".format(a, b, c, d))

        print("\n")

    @staticmethod
    def select_move(api_handler: APIHandler) -> str:
        """
        Displays the input field for the user to select and search for a move

        Parameters:
        api_handler: APIHandler
            The APIHandler object used to make api calls

        Returns:
        String of the users input from the PyInquirer prompt
        """

        search_move: list = [
            {
                "type": "input",
                "name": "search_move",
                "message": "What is the name or move number you would like to search for?",
                "validate": lambda val: api_handler.get_move(val.lower().strip(" ")).status_code != 404 or  # noqa: W504
                "Move not found, please check you have input the correct name/number"
            }
        ]

        return prompt(search_move)["search_move"].lower().strip(" ")

    @staticmethod
    def confirm_move() -> str:
        """
        Get confirmation to add the move to the currently selected move slot

        Returns:
        String of the users input from the PyInquirer prompt
        """

        confirm_move: list = [
            {
                "type": "list",
                "name": "confirm_move",
                "message": "Add this move to your Pokémon?",
                "choices": [
                    "Add move",
                    "Search for another move"
                ]
            }
        ]

        return prompt(confirm_move)["confirm_move"]
