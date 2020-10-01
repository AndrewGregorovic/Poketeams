import json

from PyInquirer import prompt, Separator  # type: ignore

from move import Move


class Pokemon():

    def __init__(self, id, name, types, weight, height,
                 abilities, move_list, move_set):
        self.id = id
        self.name = name
        self.types = types
        self.weight = weight
        self.height = height
        self.abilities = abilities
        self.move_list = move_list
        self.move_set = move_set

    @classmethod
    def from_json(cls, data):
        moves = list(map(Move.from_json, data["move_set"]))
        return cls(data["id"], data["name"], data["types"], data["weight"],
                   data["height"], data["abilities"], data["move_list"], moves)

    @classmethod
    def from_response(cls, api_handler, response):
        api_data = json.loads(response.text)
        id = api_data["id"]
        name = api_data["name"].capitalize()
        types = tuple([type["type"]["name"].capitalize() for type in api_data["types"]])
        weight = api_data["weight"]
        height = api_data["height"]
        abilities = {}
        for ability in api_data["abilities"]:
            r = json.loads(api_handler.get_ability(ability["ability"]["name"]).text)
            for effect_entry in r["effect_entries"]:
                if effect_entry["language"]["name"] == "en":
                    abilities[ability["ability"]["name"].capitalize()] = effect_entry["effect"]
        move_list = [move["move"]["name"].capitalize() for move in api_data["moves"]]
        default_move = ["None", "None", "None", "None", "None", "None", "None"]
        if len(move_list) < 4:
            move_set = [Move(*default_move) for i in range(len(move_list))]
        else:
            move_set = [Move(*default_move) for i in range(4)]
        return cls(id, name, types, weight, height, abilities, move_list, move_set)

    def view_pokemon(self, team_name, team_choice):
        print(f"Team: {team_name}")
        print(f"Slot #{team_choice + 1}\n\n")
        print(f"Name: {self.name}")
        print(f"Pokedex ID: {self.id}\n")
        print(f"Height: {self.height} decimetres")
        print(f"Weight: {self.weight} hectograms\n")
        if len(self.types) == 2:
            print(f"Types: {self.types[0]}")
            print(f"       {self.types[1]}")
        else:
            print(f"Type: {self.types[0]}")
        print("")
        print("Abilities:")
        for ability in self.abilities:
            # need to do api calls to pull ability effect info
            print(f"  - {ability}:")
            print(f"      {self.abilities[ability]}")
        print("")
        print("Current Move Set:")
        print(f"  - {self.move_set[0].name}")
        print(f"  - {self.move_set[1].name}")
        print(f"  - {self.move_set[2].name}")
        print(f"  - {self.move_set[3].name}")
        print("\n")

    def get_pokemon_options(self, mode):
        options = [
            "Change Pokemon",
            None,
            "Back to team view"
        ]

        if mode == "online":
            if self.name == "None":
                options[1] = {"name": "Change moves",
                              "disabled": "Cannot change moves on an empty pokemon slot"}
            else:
                options[1] = "Change moves"

            return options

        else:
            if self.name == "None":
                options[1] = {"name": "View moves",
                              "disabled": "Cannot view moves on an empty pokemon slot"}
            else:
                options[1] = "View moves"

            return options[1:]

    def pokemon_menu(self, mode):
        pokemon_options = [
            {
                "type": "list",
                "name": "pokemon_menu",
                "message": "What would you like to do with this pokemon slot?",
                "choices": self.get_pokemon_options(mode)
            }
        ]

        pokemon_option = prompt(pokemon_options)["pokemon_menu"]

        if pokemon_option == "Change moves" or pokemon_option == "View moves":
            select_pokemon_move = [
                {
                    "type": "list",
                    "name": "select_pokemon_move",
                    "message": "Which move slot would you like to select?",
                    "choices": [
                        "Slot 1 - " + (self.move_set[0].name
                                       if self.move_set[0].name != "None"
                                       else "Empty"),
                        "Slot 2 - " + (self.move_set[1].name
                                       if self.move_set[1].name != "None"
                                       else "Empty"),
                        "Slot 3 - " + (self.move_set[2].name
                                       if self.move_set[2].name != "None"
                                       else "Empty"),
                        "Slot 4 - " + (self.move_set[3].name
                                       if self.move_set[3].name != "None"
                                       else "Empty")
                    ]
                }
            ]

            return int(
                prompt(select_pokemon_move)["select_pokemon_move"][5]) - 1
        else:
            return pokemon_option

    def select_pokemon(self, api_handler):
        print("\nIf you are unsure of what Pokémon you would like to search "
              "for, select a Pokémon generation to view the list of Pokémon "
              "from that generation.\n\nOnce you know what Pokémon you would "
              "like to search for, select the Search option and enter the "
              "Pokémon's name or pokedex number. If the Pokémon you are "
              "searching for has different forms, enter the Pokémon's name "
              "followed by -<form> where <form> is the Pokémon's form you "
              "are interested in, some generation lists will show examples."
              "\n")
        select_pokemon_options = [
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

        selection = prompt(select_pokemon_options)["select_pokemon_option"]

        if selection == "Search":
            search_pokemon = [
                {
                    "type": "input",
                    "name": "search_pokemon",
                    "message": "What is the name or Pokédex # you would like to search for?",
                    "validate": lambda val: api_handler.get_pokemon(val).status_code != 404 or "Pokémon not found, please check you have input the correct name/number"
                }
            ]

            return prompt(search_pokemon)["search_pokemon"]

        else:
            return selection

    def view_pokemon_list(self, view_list, number, response):
        api_data = json.loads(response.text)
        pokemon_list = []
        for result in api_data["results"]:
            pokemon_list.append(f" #{number} {result['name'].capitalize()} ")
            number += 1

        while len(pokemon_list) % 4 != 0:
            pokemon_list.append("")

        print(f"{view_list} Pokémon:\n")
        for a, b, c, d, e in zip(pokemon_list[::5], pokemon_list[1::5], pokemon_list[2::5], pokemon_list[3::5], pokemon_list[4::5]):
            print("{:<27}{:<27}{:<27}{:<27}{:<27}".format(a, b, c, d, e))

    def confirm_pokemon(self):
        confirm_pokemon = [
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

    def view_move_list(self):
        pass
