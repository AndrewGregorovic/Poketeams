import requests
import json
from PyInquirer import prompt, Separator

# Additional feature if time, have offline mode to only view saved teams
class Data():
    team_data_path = "json/team_data.json"
    current_team = None

    def __init__(self):
        try:
            with open(team_data_path, "r") as f:
                self.team_data = json.loads(f.read())
        except:
            self.team_data = []

    def convert_to_objects(self):
        pass

    def get_main_menu_options(self):
        options = [
            "Create a new team",
            None,
            None,
            Separator(),
            "Quit"
        ]

        if self.team_data == []:
            options[1] = { "name": "Select a saved team", "disabled": "No saved teams" }
            options[2] = { "name": "Delete a saved team", "disabled": "No saved teams" }
        else:
            options[1] = "Select a saved team"
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

        self.current_team = Team(prompt(new_team_name)["new_team_name"])
        
        # Additional functionality, warn if name is already used 

    def list_saved_teams(self):
        print("Currently saved teams:")
        for team in self.team_data:
            print(f" - {team[team_name]}")

    def select_saved_team(self):
        if self.team_data != []:
            self.list_saved_teams()
            self.current_team = input("Which team would you like to select?: ")
        else:
            print("There are no saved teams.")
            list_ask_new = input("Would you like to create a new team?: ")
            if list_ask_new in ("y", "yes"):
                self.new_team()

    def delete_saved_team(self):
        if self.team_data != []:
            while True:
                self.list_saved_teams()
                while True:
                    delete_team = input("Which team would you like to delete?: ")
                    if delete_team not in [team[team_name] for team in self.team_data]:
                        print("Unable to find a team named {delete_team}, please check that the name has been spelt correctly.")
                    else:
                        break
                for team in self.team_data:
                    if team[team_name] == delete_team:
                        self.team_data.remove(team)
                        print(f"{delete_team} has been deleted.")
                delete_another = input("Would you like to delete another team?: ")
                if delete_another not in ("y", "yes"):
                    break
        else:
            print("There are no saved teams to delete.")

class Team():
    pokemon_list = [None, None, None, None, None, None]

    def __init__(self, name):
        self.name = name

    def view_team(self):
        print(f"Team: {self.name}\n")
        for i in range(6):
            print(f"Pokemon {i + 1}:")
            if self.pokemon_list[i]:
                print(f"    {self.pokemon_list[i].name}\n")
            else:
                print("    Empty\n")

class Pokemon():
    move_list = [None, None, None, None]

    def __init__(self, response):
        self.id = None
        self.name = None
        self.types = ()
        self.weight = None
        self.height = None
        self.abilities = {}

    def view_pokemon(self):
        pass

class APIHandler():
    api_url = "https://pokeapi.co/api/v2/"

    def get_pokemon(self, name, query_string = ""):
        request_url = api_url + "pokemon/" + name + query_string
        return json.loads(requests.get(request_url).text)

    def get_move(self, name):
        request_url = api_url + "move/" + name
        return json.loads(requests.get(request_url).text)


print("Poketeams")
print("Build your pokemon dream teams")
api_handler = APIHandler()
team_controller = Data()
while True:
    choice = team_controller.main_menu_select()
    if choice == "Create a new team":
        team_controller.new_team()
        team_controller.current_team.view_team()
    else:
        exit()