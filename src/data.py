import json
import os
from typing import Union

from PyInquirer import prompt, Separator  # type: ignore

from move import Move
from pokemon import Pokemon
from team import Team


class Data():

    def __init__(self, name: str) -> None:

        self.current_team: Union[None, Team] = None
        self.default_move: list = ["None", 0, 0, 0, ("None",), 0, "None"]
        self.default_pokemon: list = [0, "None", ("None",), 0, 0, {"None": "None"}, [],
                                      [Move(*self.default_move), Move(*self.default_move), Move(*self.default_move), Move(*self.default_move)]]
        self.default_pokemon_list: list = [Pokemon(*self.default_pokemon), Pokemon(*self.default_pokemon), Pokemon(*self.default_pokemon),
                                           Pokemon(*self.default_pokemon), Pokemon(*self.default_pokemon), Pokemon(*self.default_pokemon)]

        # Create different json files for testing and actually using the app
        if name == "test":
            self.team_data_path: str = os.path.dirname(os.path.abspath(__file__)) + "/json/test_data.json"
        else:
            self.team_data_path = os.path.dirname(os.path.abspath(__file__)) + "/json/team_data.json"

        # Try to create the /json directory to be sure that it's there
        try:
            os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "/json")
        except FileExistsError:
            pass

        try:
            with open(self.team_data_path, "r") as f:
                self.team_data: list = self.convert_to_objects(json.loads(f.readline()))
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.team_data = []

    @staticmethod
    def convert_to_objects(json_data: list) -> list:
        """Passes each set of team data to the Team.from_json() class method to create the Team class"""
        converted_data: list = []
        for team in json_data:
            converted_data.append(Team.from_json(team))

        return converted_data

    def get_main_menu_options(self, mode: str) -> list:
        """Determine which main menu options should be present and enabled"""
        options: list = [
            "Create a new team",
            None,
            None,
            Separator(),
            "Quit"
        ]

        if self.team_data == []:
            options[1] = {"name": "Load a saved team",
                          "disabled": "No saved teams"}
            options[2] = {"name": "Delete a saved team",
                          "disabled": "No saved teams"}
        else:
            options[1] = "Load a saved team"
            options[2] = "Delete a saved team"

        if mode == "online":
            return options
        else:
            return options[1:]

    def main_menu_select(self, mode: str) -> str:
        """Display the main menu options"""
        main_menu_options: list = [
            {
                "type": "list",
                "name": "main_menu_option",
                "message": "What would you like to do?",
                "choices": self.get_main_menu_options(mode)
            }
        ]

        # Ensure that a disabled option can't be selected even if it's the default selection
        while True:
            main_menu_option: str = prompt(main_menu_options)["main_menu_option"]
            if main_menu_option not in main_menu_options[0]["choices"]:
                print("Can't select a disabled option, please try again.\n")
            else:
                break

        return main_menu_option

    def new_team_name(self) -> str:
        """Get user input for the team name"""
        new_team_name: list = [
            {
                "type": "input",
                "name": "new_team_name",
                "message": "What would you like to name this team?:",
                "default": "New Team",
                "validate": lambda val: val.strip(" ") not in [team.name for team in self.team_data] + [""] or  # noqa: W504
                "Invalid name. Must contain at least 1 non-space character and not be in use by a currently saved team."
            }
        ]

        return prompt(new_team_name)["new_team_name"]

    def select_saved_team(self) -> str:
        """Get user's selection for which team to load or delete"""
        saved_team_choice: list = [
            {
                "type": "list",
                "name": "saved_team_choice",
                "message": "Which saved team would you like to select?",
                "choices": [team.name for team in self.team_data]
            }
        ]

        return prompt(saved_team_choice)["saved_team_choice"]

    def load_saved_team(self) -> None:
        """Load selected team"""
        selected_team: str = self.select_saved_team()

        for team in self.team_data:
            if team.name == selected_team:
                self.current_team = team

    def delete_saved_team(self) -> None:
        """Delete selected team"""
        selected_team: str = self.select_saved_team()

        for team in self.team_data:
            if team.name == selected_team:
                self.team_data.remove(team)
                print(f"{selected_team} has been deleted.")
                self.current_team = None

    def save_all_teams(self) -> tuple:
        """Write the team data to .json file after converting it to json"""
        try:
            if self.team_data != []:
                json_team_data = json.dumps(self.team_data, default=lambda o: o.__dict__)

                with open(self.team_data_path, "w") as f:
                    f.write(json_team_data)
            else:
                with open(self.team_data_path, "w") as f:
                    pass

            return (True, "")
        except Exception as e:
            return (False, e)
