import requests
import json

class Data():
    team_data_path = "json/team_data.json"
    current_team = None

    def __init__(self):
        try:
            with open(team_data_path, "r") as f:
                self.team_data = json.loads(f.read())
        except:
            self.team_data = []

    def new_team(self):
        new_name = input("What would you like to name this new team?: ")
        self.current_team = Team(new_name)

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
            while:
                self.list_saved_teams()
                while:
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

class Pokemon():
    move_list = [None, None, None, None]

    def __init__(self, name):
        self.name = name

class APIHandler():
    api_url = "https://pokeapi.co/api/v2/"

    def get_pokemon(self, name):
        request_url = api_url + "pokemon/" + name
        return json.loads(requests.get(request_url).text)