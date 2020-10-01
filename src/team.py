from PyInquirer import prompt  # type: ignore

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

    def get_team_menu_options(self, mode):
        options = [
            None,
            "Rename team",
            "Save team",
            "Back to main menu"
        ]

        empty_team = True
        for pokemon in self.pokemon_list:
            if pokemon.name != "None":
                empty_team = False

        if mode == "online":
            options[0] = "Edit team"
        elif mode == "offline" and empty_team is True:
            options[0] = {"name": "View Pokemon",
                          "disabled": "There are no Pokemon saved to this team"}
        else:
            options[0] = "View Pokemon"

        return options

    def team_menu(self, mode):
        team_options = [
            {
                "type": "list",
                "name": "team_menu",
                "message": "What would you like to do with this team?",
                "choices": self.get_team_menu_options(mode)
            }
        ]

        while True:
            team_option = prompt(team_options)["team_menu"]
            if team_option not in team_options[0]["choices"]:
                print("Can't select a disabled option, please try again.\n")
            else:
                break

        if team_option == "Edit team" or team_option == "View Pokemon":
            select_team_pokemon = [
                {
                    "type": "list",
                    "name": "select_team_pokemon",
                    "message": "Which Pokemon slot would you like to select?",
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
