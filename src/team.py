from PyInquirer import prompt
from pokemon import Pokemon


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
                        "Slot 1 - " + (self.pokemon_list[0].name
                                       if self.pokemon_list[0].name != "None"
                                       else "Empty"),
                        "Slot 2 - " + (self.pokemon_list[1].name
                                       if self.pokemon_list[1].name != "None"
                                       else "Empty"),
                        "Slot 3 - " + (self.pokemon_list[2].name
                                       if self.pokemon_list[2].name != "None"
                                       else "Empty"),
                        "Slot 4 - " + (self.pokemon_list[3].name
                                       if self.pokemon_list[3].name != "None"
                                       else "Empty"),
                        "Slot 5 - " + (self.pokemon_list[4].name
                                       if self.pokemon_list[4].name != "None"
                                       else "Empty"),
                        "Slot 6 - " + (self.pokemon_list[5].name
                                       if self.pokemon_list[5].name != "None"
                                       else "Empty")
                    ]
                }
            ]

            return int(
                prompt(select_team_pokemon)["select_team_pokemon"][5]) - 1
        else:
            return team_option

# saving a new team works but need to check
# that team correctly updates with new data
    def team_save(self, team_data):
        # add/update team_controller.team_data attribute
        if team_data != []:
            for team in team_data:
                if team.name == self.name:
                    team = self
                    return team_data

            team_data.append(self)
        else:
            team_data.append(self)

        return team_data
