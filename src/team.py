from PyInquirer import prompt  # type: ignore

from pokemon import Pokemon


class Team():

    def __init__(self, name: str, pokemon_list: list) -> None:
        self.name: str = name
        self.pokemon_list: list = pokemon_list

    @classmethod
    def from_json(cls, data: dict) -> "Team":
        """Passes each pokémon dictionary to Pokemon.from_json() to create a Pokemon class and then returns a Team class"""
        pokemon: list = list(map(Pokemon.from_json, data["pokemon_list"]))
        return cls(data["name"], pokemon)

    def view_team(self) -> None:
        """Display the team overview"""
        print(f"\n\u001b[1m\u001b[4mTeam\u001b[0m: \u001b[7m {self.name} \u001b[0m\n")

        for i in range(6):
            print(f"\u001b[4mPokémon {i + 1}\u001b[0m:\n")
            if self.pokemon_list[i]:
                print(f"    \u001b[1mName\u001b[0m: {self.pokemon_list[i].name}\n")
                if len(self.pokemon_list[i].move_set) > 0:
                    print(f"    \u001b[1mCurrent Move Set\u001b[0m: {', '.join([move.name for move in self.pokemon_list[i].move_set]).strip(', ')}\n")
                else:
                    print("    \u001b[1mCurrent Move Set\u001b[0m: This Pokemon cannot learn any moves.\n")
            else:
                print("    Empty\n")

        print()

    def get_team_menu_options(self, mode: str) -> list:
        """Determines which options are shown and enabled depending on app mode and if the team is empty"""
        options: list = [
            None,
            "Rename team",
            "Save team",
            "Back to main menu"
        ]

        empty_team: bool = True
        for pokemon in self.pokemon_list:
            if pokemon.name != "None":
                empty_team = False

        if mode == "online":
            options[0] = "Edit team"
        elif mode == "offline" and empty_team is True:
            options[0] = {"name": "View Pokémon",
                          "disabled": "There are no Pokémon saved to this team"}
        else:
            options[0] = "View Pokémon"

        return options

    def team_menu(self, mode: str) -> str:
        """Displays the menu options for team view"""
        team_options: list = [
            {
                "type": "list",
                "name": "team_menu",
                "message": "What would you like to do with this team?",
                "choices": self.get_team_menu_options(mode)
            }
        ]

        while True:
            team_option: str = prompt(team_options)["team_menu"]
            if team_option not in team_options[0]["choices"]:
                print("Can't select a disabled option, please try again.\n")
            else:
                break

        if team_option == "Edit team" or team_option == "View Pokémon":
            select_team_pokemon: list = [
                {
                    "type": "list",
                    "name": "select_team_pokemon",
                    "message": "Which Pokémon slot would you like to select?",
                    "choices": [
                        "Slot 1 - " + (self.pokemon_list[0].name if self.pokemon_list[0].name != "None" else "Empty"),
                        "Slot 2 - " + (self.pokemon_list[1].name if self.pokemon_list[1].name != "None" else "Empty"),
                        "Slot 3 - " + (self.pokemon_list[2].name if self.pokemon_list[2].name != "None" else "Empty"),
                        "Slot 4 - " + (self.pokemon_list[3].name if self.pokemon_list[3].name != "None" else "Empty"),
                        "Slot 5 - " + (self.pokemon_list[4].name if self.pokemon_list[4].name != "None" else "Empty"),
                        "Slot 6 - " + (self.pokemon_list[5].name if self.pokemon_list[5].name != "None" else "Empty")
                    ]
                }
            ]

            return prompt(select_team_pokemon)["select_team_pokemon"][5]
        else:
            return team_option

    def team_save(self, team_data: list) -> list:
        """Saves the current team to the Data.team_data attribute"""
        team_names: list = [team.name for team in team_data]
        if self.name in team_names:
            i: int = team_names.index(self.name)
            team_data[i] = self
            return team_data
        else:
            team_data.append(self)
            return team_data
