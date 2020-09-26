from PyInquirer import prompt, Separator
from move import Move

class Pokemon():

    def __init__(self, id, name, types, weight, height, abilities, move_list, move_set):
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
        return cls(data["id"], data["name"], data["types"], data["weight"], data["height"], data["abilities"], data["move_list"], moves)

    def view_pokemon(self, team_name, team_choice):
        print(f"Team: {team_name}")
        print(f"Slot #{team_choice + 1}\n")
        print(f"Name: {self.name}")
        print(f"Pokedex ID: {self.id}\n")
        print(f"Height: {self.height} decimetres")
        print(f"Weight: {self.weight} hectograms\n")
        if len(self.types) == 2:
            print(f"Types: {self.types[0]}")
            print(f"         {self.types[1]}")
        elif len(self.types) == 1:
            print(f"Type: {self.types[0]}")
        else:
            print(f"Type: None")
        print("")
        print(f"Abilities: ") # Fix this later
        print("")
        print(f"Current Move Set:")

    def pokemon_menu(self):
        pokemon_options = [
            {
                "type": "list",
                "name": "pokemon_menu",
                "message": "What would you like to do with this pokemon slot?",
                "choices": [
                    "Change Pokemon",
                    "Change moves",
                    "Back to team view"
                ]
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
                        "Slot 1 - " + (self.move_set[0].name if self.move_set[0].name != "None" else "Empty"),
                        "Slot 2 - " + (self.move_set[1].name if self.move_set[1].name != "None"else "Empty"),
                        "Slot 3 - " + (self.move_set[2].name if self.move_set[2].name != "None" else "Empty"),
                        "Slot 4 - " + (self.move_set[3].name if self.move_set[3].name != "None" else "Empty")
                    ]
                }
            ]

            return int(prompt(select_pokemon_move)["select_pokemon_move"][5]) - 1
        else:
            return pokemon_option
