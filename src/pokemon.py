from PyInquirer import prompt

from move import Move


class Pokemon():

    def __init__(self, id, name, types, weight, height,
                 abilities, move_list, move_set):
        self.id = "None"
        self.name = "None"
        self.types = ("None")
        self.weight = "None"
        self.height = "None"
        self.abilities = {"Ability 1": "None"}
        self.move_list = "None"
        self.move_set = move_set

    @classmethod
    def from_json(cls, data):
        moves = list(map(Move.from_json, data["move_set"]))
        return cls(data["id"], data["name"], data["types"], data["weight"],
                   data["height"], data["abilities"], data["move_list"], moves)

    def view_pokemon(self, team_name, team_choice):
        print(f"Team: {team_name}\n")
        print(f"Slot #{team_choice + 1}\n\n")
        print(f"Name: {self.name}")
        print(f"Pokedex ID: {self.id}\n")
        print(f"Height: {self.height} decimetres")
        print(f"Weight: {self.weight} hectograms\n")
        if len(self.types) == 2:
            print(f"Types: {self.types[0]}")
            print(f"         {self.types[1]}")
        else:
            print(f"Type: {self.types}")
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

    def get_pokemon_options(self):
        options = [
                    "Change Pokemon",
                    None,
                    "Back to team view"
        ]

        if self.name == "None":
            options[1] = {"name": "Change moves",
                          "disabled": "Cannot change moves on an empty pokemon slot"}
        else:
            options[1] = "Change moves"

        return options

    def pokemon_menu(self):
        pokemon_options = [
            {
                "type": "list",
                "name": "pokemon_menu",
                "message": "What would you like to do with this pokemon slot?",
                "choices": self.get_pokemon_options()
            }
        ]

        pokemon_option = prompt(pokemon_options)["pokemon_menu"]

        if pokemon_option == "Change moves":
            select_pokemon_move = [
                {
                    "type": "list",
                    "name": "select_pokemon_move",
                    "message": "Which move slot would you like to change?",
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

    def select_pokemon(self):
        pass

    def view_pokemon_list(self):
        pass

    def search_pokemon(self):
        pass

    def confirm_pokemon(self):
        pass

    def view_move_list(self):
        pass
