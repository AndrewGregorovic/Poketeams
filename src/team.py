from PyInquirer import prompt  # type: ignore

from pokemon import Pokemon


class Team():
    """
    A class to represent a pokemon team

    Attributes:
    name: str
        Name of the pokemon team
    pokemon_list: list
        The list of Pokemon objects that make up the team

    Methods:
    from_json(cls, data: dict)
        Creates a Team object from a json dictionary

    view_team(self)
        Displays the Team object's information

    get_team_menu_options(self, mode: str)
        Gets the options to use in Team.team_menu()

    get_team_slot_options(self, mode: str)
        Gets the team slot options to use in Team.team_menu()

    team_menu(self, mode: str)
        Displays the menu for the Team screen

    team_save(self, team_data: list)
        Updates the Data class' team_data attribute with the current teams data
    """

    def __init__(self, name: str, pokemon_list: list) -> None:
        """
        Sets the required attributes for the Team object

        Parameters:
        name: str
            Name of the pokemon team
        pokemon_list: list
            The list of Pokemon objects that make up the team
        """

        self.name: str = name
        self.pokemon_list: list = pokemon_list

    @classmethod
    def from_json(cls, data: dict) -> "Team":
        """
        Creates a Team object from a json dictionary

        Parameters:
        data: dict
            Dictionary containing attribute, value pairs from the applications saved json data

        Returns:
        Team object
        """

        pokemon: list = list(map(Pokemon.from_json, data["pokemon_list"]))
        return cls(data["name"], pokemon)

    def view_team(self) -> None:
        """
        Displays the Team object's information

        Returns:
        None
        """

        print(f"\n\u001b[1m\u001b[4mTeam\u001b[0m: \u001b[7m {self.name} \u001b[0m\n")

        for i in range(6):
            print(f"\u001b[4mPokémon {i + 1}\u001b[0m:\n")
            if self.pokemon_list[i]:
                print(f"    \u001b[1mName\u001b[0m: {self.pokemon_list[i].name}\n")
                if len(self.pokemon_list[i].move_set) > 0:
                    print(f"    \u001b[1mCurrent Move Set\u001b[0m: {', '.join([move.name for move in self.pokemon_list[i].move_set]).strip(', ')}\n")
                else:
                    print("    \u001b[1mCurrent Move Set\u001b[0m: This Pokémon cannot learn any moves.\n")
            else:
                print("    Empty\n")

        print("")

    def get_team_menu_options(self, mode: str) -> list:
        """
        Gets the options to use in Team.team_menu()

        Parameters:
        mode: str
            The currently running mode of the application

        Returns:
        List of menu options to display in Team.team_menu()
        """

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

    def get_team_slot_options(self, mode: str) -> list:
        """
        Gets the team slot options to use in Team.team_menu()

        Parameters:
        mode: str
            The currently running mode of the application

        Returns:
        List of pokemon slot options to display in Team.team_menu()
        """

        if mode == "online":
            team_slots = [
                "Slot 1 - " + (self.pokemon_list[0].name if self.pokemon_list[0].name != "None" else "Empty"),
                "Slot 2 - " + (self.pokemon_list[1].name if self.pokemon_list[1].name != "None" else "Empty"),
                "Slot 3 - " + (self.pokemon_list[2].name if self.pokemon_list[2].name != "None" else "Empty"),
                "Slot 4 - " + (self.pokemon_list[3].name if self.pokemon_list[3].name != "None" else "Empty"),
                "Slot 5 - " + (self.pokemon_list[4].name if self.pokemon_list[4].name != "None" else "Empty"),
                "Slot 6 - " + (self.pokemon_list[5].name if self.pokemon_list[5].name != "None" else "Empty")
            ]
        else:
            team_slots = []
            for i in range(6):
                if self.pokemon_list[i].name != "None":
                    team_slots.append(f"Slot {i + 1} - {(self.pokemon_list[i].name)}")
                else:
                    team_slots.append({"name": f"Slot {i + 1} - Empty",
                                       "disabled": "There is no Pokémon saved to this slot"})

        return team_slots

    def team_menu(self, mode: str) -> str:
        """
        Displays the menu for the Team screen

        Parameters:
        mode: str
            The currently running mode of the application

        Returns:
        String of the user's input from the PyInquirer prompts
        """

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
                    "choices": self.get_team_slot_options(mode)
                }
            ]

            return prompt(select_team_pokemon)["select_team_pokemon"][5]
        else:
            return team_option

    def team_save(self, team_data: list) -> list:
        """
        Updates the Data class' team_data attribute with the current teams data

        Parameters:
        team_data: list
            The Data class' team_data attribute with all team data loaded from json and from current session

        Returns:
        Updated list of team data to be reassigned to the Data class' team_data attribute
        """

        team_names: list = [team.name for team in team_data]
        if self.name in team_names:
            i: int = team_names.index(self.name)
            team_data[i] = self
            return team_data
        else:
            team_data.append(self)
            return team_data
