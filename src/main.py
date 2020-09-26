import requests
import json
from PyInquirer import prompt, Separator
import os
from copy import deepcopy


class Move():

    def __init__(self, name, accuracy, power, pp, types, effect_chance, effect):
        self.name = "None"
        self.accuracy = "None"
        self.power = "None"
        self.pp = "None"
        self.types = ("None")
        self.effect_chance = "None"
        self.effect = "None"

    @classmethod
    def from_json(cls, data):
        return cls(**data)

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

    def view_pokemon(self):
        print(f"Team: {team_controller.current_team.name}")
        print(f"Slot #{team_choice + 1}\n")
        print(f"Name: {self.name}")
        print(f"Pokedex ID: {self.id}\n")
        print(f"Height: {self.height} decimeters")
        print(f"Weight: {self.weight} kilograms\n")
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
                        "Slot 1 - " + (self.move_set[0].name if self.move_set[0] != None else "Empty"),
                        "Slot 2 - " + (self.move_set[1].name if self.move_set[1] != None else "Empty"),
                        "Slot 3 - " + (self.move_set[2].name if self.move_set[2] != None else "Empty"),
                        "Slot 4 - " + (self.move_set[3].name if self.move_set[3] != None else "Empty")
                    ]
                }
            ]

            return int(prompt(select_pokemon_move)["select_pokemon_move"][5]) - 1
        else:
            return pokemon_option

class Team():

    def __init__(self, name, pokemon_list):
        self.name = name
        self.pokemon_list = pokemon_list

    @classmethod
    def from_json(cls, data):
        pokemon = list(map(Pokemon.from_json, data["pokemon_list"]))
        return cls(data["name"], pokemon)

    def view_team(self):
        print(f"Team: {self.name}\n")
        for i in range(6):
            print(f"Pokemon {i + 1}:")
            if self.pokemon_list[i]:
                print(f"    {self.pokemon_list[i].name}\n")
            else:
                print("    Empty\n")

    def team_menu(self):
        team_options = [
            {
                "type": "list",
                "name": "team_menu",
                "message": "What would you like to do with this team?",
                "choices": [
                    "Edit team",
                    "Save team",
                    "Back to main menu"
                ]
            }
        ]

        team_option = prompt(team_options)["team_menu"]

        if team_option == "Edit team":
            select_team_pokemon = [
                {
                    "type": "list",
                    "name": "select_team_pokemon",
                    "message": "Which Pokemon slot would you like to change?",
                    "choices": [
                        "Slot 1 - " + (self.pokemon_list[0].name if self.pokemon_list[0] != None else "Empty"),
                        "Slot 2 - " + (self.pokemon_list[1].name if self.pokemon_list[1] != None else "Empty"),
                        "Slot 3 - " + (self.pokemon_list[2].name if self.pokemon_list[2] != None else "Empty"),
                        "Slot 4 - " + (self.pokemon_list[3].name if self.pokemon_list[3] != None else "Empty"),
                        "Slot 5 - " + (self.pokemon_list[4].name if self.pokemon_list[4] != None else "Empty"),
                        "Slot 6 - " + (self.pokemon_list[5].name if self.pokemon_list[5] != None else "Empty")
                    ]
                }
            ]

            return int(prompt(select_team_pokemon)["select_team_pokemon"][5]) - 1
        else:
            return team_option

    def team_save(self):
        # add/update team_controller.team_data attribute
        if team_controller.team_data != []:
            for team in team_controller.team_data:
                if team.name == current_team.name:
                    team = current_team
                    return
            
            team_controller.team_data.append(current_team)
        else:
            team_controller.team_data.append(current_team)

class APIHandler():
    api_url = "https://pokeapi.co/api/v2/"

    def get_pokemon(self, name, query_string = ""):
        request_url = api_url + "pokemon/" + name + query_string
        return json.loads(requests.get(request_url).text)

    def get_move(self, name):
        request_url = api_url + "move/" + name
        return json.loads(requests.get(request_url).text)

# Additional feature if time, have offline mode to only view saved teams
class Data():
    team_data_path = os.path.dirname(os.path.abspath(__file__)) + "/json/team_data.json"
    current_team = None
    default_move = ["None", "None", "None", "None", "None", "None", "None"]
    default_pokemon = ["None", "None", "None", "None", "None", "None", "None", [Move(*default_move), Move(*default_move), Move(*default_move), Move(*default_move)]]
    default_pokemon_list = [Pokemon(*default_pokemon), Pokemon(*default_pokemon), Pokemon(*default_pokemon), Pokemon(*default_pokemon), Pokemon(*default_pokemon), Pokemon(*default_pokemon)]

    def __init__(self):
        try:
            os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "/json")
        except FileExistsError:
            pass

        try:
            with open(self.team_data_path, "r") as f:
                json_data = json.loads(f.readline())
                self.team_data = self.convert_to_objects(json.loads(json_data))
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.team_data = []

    def convert_to_objects(self, json_data):
        converted_data = []
        for team in json_data:
            converted_data.append(Team.from_json(team))
            
        return converted_data

    def get_main_menu_options(self):
        options = [
            "Create a new team",
            None,
            None,
            Separator(),
            "Quit"
        ]

        if self.team_data == []:
            options[1] = { "name": "Load a saved team", "disabled": "No saved teams" }
            options[2] = { "name": "Delete a saved team", "disabled": "No saved teams" }
        else:
            options[1] = "Load a saved team"
            options[2] = "Delete a saved team"
        
        return options

    def main_menu_select(self):
        main_menu_options = [
            {
                "type": "list",
                "name": "main_menu_option",
                "message": "What would you like to do?",
                "choices": self.get_main_menu_options()
            }
        ]

        return prompt(main_menu_options)["main_menu_option"]

    def new_team(self):
        new_team_name = [
            {
                "type": "input",
                "name": "new_team_name",
                "message": "What would you like to name this new team?:",
                "default": "New Team",
                "validate": lambda val: val not in [team.name for team in self.team_data] or "Name already in use, please delete the team first to be able to use this name again"
            }
        ]

        self.current_team = Team(prompt(new_team_name)["new_team_name"], self.default_pokemon_list)

    def select_saved_team(self):
        saved_team_choice = [
            {
                "type": "list",
                "name": "saved_team_choice",
                "message": "Which saved team would you like to select?",
                "choices": [team.name for team in self.team_data]
            }
        ]

        return prompt(saved_team_choice)["saved_team_choice"]

    def load_saved_team(self):

        selected_team = self.select_saved_team()

        for team in self.team_data:
            if team.name == selected_team:
                self.current_team = team

    def delete_saved_team(self):
        
        selected_team = self.select_saved_team()

        for team in self.team_data:
            if team.name == selected_team:
                self.team_data.remove(team)
                print(f"{selected_team} has been deleted.")
                self.current_team = None

    def save_all_teams(self):
        # save to json file
        if self.team_data != []:
            json_team_data = json.dumps(self.team_data, default=lambda o: o.__dict__)
            with open(self.team_data_path, "w") as f:
                json_string = json.dumps(json_team_data)
                f.write(json_string)
        else:
            with open(self.team_data_path, "w") as f:
                pass



print("Poketeams")
print("Build your pokemon dream teams")
api_handler = APIHandler()
team_controller = Data()
while True:
    choice = team_controller.main_menu_select()
    if choice == "Create a new team":
        team_controller.new_team()
    elif choice == "Load a saved team":
        team_controller.load_saved_team()
    elif choice == "Delete a saved team":
        team_controller.delete_saved_team()
        team_controller.save_all_teams()
    else:
        team_controller.save_all_teams()
        exit()

    current_team = team_controller.current_team
    while current_team != None:
        current_team.view_team()
        team_choice = current_team.team_menu()
        if team_choice == "Save team":
            current_team.team_save()
            team_controller.save_all_teams()
        elif team_choice == "Back to main menu":
            current_team.team_save()
            team_controller.save_all_teams()
            break
        else:
            current_pokemon = current_team.pokemon_list[team_choice]
            current_pokemon.view_pokemon()
            pokemon_choice = current_pokemon.pokemon_menu()
            if pokemon_choice == "Change Pokemon":
                print("Pokemon selection here")
            elif pokemon_choice == "Back to team view":
                print("Back to team view here")
            else:
                print("View move here")