import json

from PyInquirer import prompt, Separator  # type: ignore
import requests

from apihandler import APIHandler
from move import Move


class Pokemon():

    def __init__(self, id: int, name: str, types: tuple, weight: int, height: int,
                 abilities: dict, move_list: list, move_set: list) -> None:
        self.id: int = id
        self.name: str = name
        self.types: tuple = types
        self.weight: int = weight
        self.height: int = height
        self.abilities: dict = abilities
        self.move_list: list = move_list
        self.move_set: list = move_set

    @classmethod
    def from_json(cls, data: dict) -> "Pokemon":
        """Passes each move dictionary to Move.from_json() to create a Move class and then returns a Pokemon class"""
        moves: list = list(map(Move.from_json, data["move_set"]))
        return cls(data["id"], data["name"], data["types"], data["weight"],
                   data["height"], data["abilities"], data["move_list"], moves)

    @classmethod
    def from_response(cls, api_handler: APIHandler, response: requests.models.Response) -> "Pokemon":
        """Pulls the desired information out of the api response and fetches additional data for abilities
        Then returns a Pokemon class using all the relevant api data and a default empty move set"""
        api_data: dict = json.loads(response.text)
        id: int = api_data["id"]
        name: str = api_data["name"].capitalize()
        types: tuple = tuple([type["type"]["name"].capitalize() for type in api_data["types"]])
        weight: int = api_data["weight"]
        height: int = api_data["height"]

        abilities: dict = {}
        for ability in api_data["abilities"]:
            r: dict = json.loads(api_handler.get_ability(ability["ability"]["name"]).text)
            for effect_entry in r["effect_entries"]:
                if effect_entry["language"]["name"] == "en":
                    abilities[ability["ability"]["name"].capitalize()] = effect_entry["effect"].replace("\n", " ").replace("  ", " ")

        move_list: list = [move["move"]["name"].capitalize() for move in api_data["moves"]]

        default_move: list = ["None", 0, 0, 0, "None", 0, "None"]
        if len(move_list) < 4:
            move_set: list = [Move(*default_move) for i in range(len(move_list))]
        else:
            move_set = [Move(*default_move) for i in range(4)]

        return cls(id, name, types, weight, height, abilities, move_list, move_set)

    def view_pokemon(self, team_name: str, team_choice: str) -> None:
        """Displays all the saved information about the current Pokemon object"""
        print(f"\n\u001b[1m\u001b[4mTeam\u001b[0m: \u001b[7m {team_name} \u001b[0m")
        print(f"\u001b[4mSlot #{int(team_choice)}\u001b[0m\n\n")
        print(f"\u001b[1mName\u001b[0m: {self.name}")
        print(f"\u001b[1mPokédex ID:\u001b[0m {self.id}\n")
        print(f"\u001b[1mHeight\u001b[0m: {self.height} decimetres")
        print(f"\u001b[1mWeight\u001b[0m: {self.weight} hectograms\n")

        if len(self.types) == 2:
            print(f"\u001b[1mTypes\u001b[0m: {self.types[0]}")
            print(f"       {self.types[1]}")
        else:
            print(f"\u001b[1mType\u001b[0m: {self.types[0]}")

        print("")
        print("\u001b[1mAbilities\u001b[0m:")
        if len(self.abilities) > 0:
            for ability in self.abilities:
                print(f"  - \u001b[4m{ability}\u001b[0m:")
                print(f"      {self.abilities[ability]}")
        else:
            print("    This Pokémon has no abilities.")

        print("")
        print("\u001b[1mCurrent Move Set\u001b[0m:")
        if len(self.move_set) > 0:
            for move in self.move_set:
                print(f"  - {move.name}")
        else:
            print("    This Pokémon cannot learn any moves.")

        print("\n")

    def get_pokemon_options(self, mode: str) -> list:
        """Determines which options are shown and enabled depending on app mode and if the move set is empty"""
        options: list = [
            "Change Pokémon",
            None,
            "Back to team view"
        ]

        if mode == "online":
            if self.name == "None":
                options[1] = {"name": "Change moves",
                              "disabled": "Cannot change moves on an empty pokémon slot"}
            else:
                options[1] = "Change moves"

            return options

        else:
            empty_move_set: bool = True
            for move in self.move_set:
                if move.name != "None":
                    empty_move_set = False

            if self.name == "None":
                options[1] = {"name": "View moves",
                              "disabled": "Cannot view moves on an empty pokémon slot"}
            elif empty_move_set:
                options[1] = {"name": "View moves",
                              "disabled": "This Pokémon does not have any moves saved"}
            else:
                options[1] = "View moves"

            return options[1:]

    def get_pokemon_move_slots_options(self, mode: str) -> list:

        if mode == "online":
            pokemon_move_slots = [
                "Slot 1 - " + (self.move_set[0].name if self.move_set[0].name != "None" else "Empty"),
                "Slot 2 - " + (self.move_set[1].name if self.move_set[1].name != "None" else "Empty"),
                "Slot 3 - " + (self.move_set[2].name if self.move_set[2].name != "None" else "Empty"),
                "Slot 4 - " + (self.move_set[3].name if self.move_set[3].name != "None" else "Empty")
            ]
        else:
            pokemon_move_slots = []
            for i in range(len(self.move_set)):
                if self.move_set[i].name != "None":
                    pokemon_move_slots.append(f"Slot {i + 1} - {self.move_set[i].name}")
                else:
                    pokemon_move_slots.append({"name": f"Slot {i + 1} - Empty",
                                               "disabled": "There is no move saved to this slot"})

        return pokemon_move_slots

    def pokemon_menu(self, mode: str) -> str:
        """Displays the menu options when viewing Pokemon information"""
        pokemon_options: list = [
            {
                "type": "list",
                "name": "pokemon_menu",
                "message": "What would you like to do with this pokémon slot?",
                "choices": self.get_pokemon_options(mode)
            }
        ]

        while True:
            pokemon_option: str = prompt(pokemon_options)["pokemon_menu"]
            if pokemon_option not in pokemon_options[0]["choices"]:
                print("Can't select a disabled option, please try again.\n")
            else:
                break

        if pokemon_option == "Change moves" or pokemon_option == "View moves":
            select_pokemon_move: list = [
                {
                    "type": "list",
                    "name": "select_pokemon_move",
                    "message": "Which move slot would you like to select?",
                    "choices": self.get_pokemon_move_slots_options(mode)
                }
            ]

            return prompt(select_pokemon_move)["select_pokemon_move"][5]
        else:
            return pokemon_option

    @staticmethod
    def select_pokemon(api_handler: APIHandler) -> str:
        """Displays the screen for selecting a Pokémon list to view and searching for a Pokémon using the api"""
        print("\nIf you are unsure of what Pokémon you would like to search for, select a Pokémon generation to view the list of Pokémon "
              "from that generation.\n\nOnce you know what Pokémon you would like to search for, select the Search option and enter the "
              "Pokémon's name or Pokédex number. If the Pokémon you are searching for has different forms, enter the Pokémon's name "
              "followed by -<form> where <form> is the Pokémon's form you are interested in, some generation lists will show examples.\n")
        select_pokemon_options: list = [
            {
                "type": "list",
                "name": "select_pokemon_option",
                "message": "What would you like to do?",
                "choices": [
                    Separator("-= View Pokémon list for: =-"),
                    "Generation 1",
                    "Generation 2",
                    "Generation 3",
                    "Generation 4",
                    "Generation 5",
                    "Generation 6",
                    "Generation 7",
                    "Generation 8",
                    Separator("-= Search for a Pokémon =-"),
                    "Search"
                ]
            }
        ]

        selection: str = prompt(select_pokemon_options)["select_pokemon_option"]

        if selection == "Search":
            search_pokemon: list = [
                {
                    "type": "input",
                    "name": "search_pokemon",
                    "message": "What is the name or Pokédex # you would like to search for?",
                    "validate": lambda val: api_handler.get_pokemon(val.lower().strip(" ")).status_code != 404 or  # noqa: W504
                    "Pokémon not found, please check you have input the correct name/number"
                }
            ]

            return prompt(search_pokemon)["search_pokemon"].lower().strip(" ")

        else:
            return selection

    @staticmethod
    def view_pokemon_list(view_list: str, number: int, response: requests.models.Response) -> None:
        """Displays the list of pokemon requested by the user in 5 even width columns"""
        api_data: dict = json.loads(response.text)
        pokemon_list: list = []
        for result in api_data["results"]:
            pokemon_list.append(f" #{number} {result['name'].capitalize()} ")
            number += 1

        while len(pokemon_list) % 5 != 0:
            pokemon_list.append("")

        print(f"\u001b[1m\u001b[4m{view_list} Pokémon\u001b[0m:\n")
        for a, b, c, d, e in zip(pokemon_list[::5], pokemon_list[1::5], pokemon_list[2::5], pokemon_list[3::5], pokemon_list[4::5]):
            print("{:<27}{:<27}{:<27}{:<27}{:<27}".format(a, b, c, d, e))

    @staticmethod
    def confirm_pokemon() -> str:
        """Displays a little confirmation menu to confirm adding the pokemon to the current team"""
        confirm_pokemon: list = [
            {
                "type": "list",
                "name": "confirm_pokemon",
                "message": "Add this Pokémon to your team?",
                "choices": [
                    "Add Pokémon",
                    "Search for another Pokémon"
                ]
            }
        ]

        return prompt(confirm_pokemon)["confirm_pokemon"]
