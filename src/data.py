import json
import os
from typing import Union

from PyInquirer import prompt, Separator  # type: ignore

from move import Move
from pokemon import Pokemon
from team import Team


class Data():
    """
    A class to control the team data that the application works with

    Attributes:
    name: str
        Name of the controller, either "main" for normal use or "test" for running the unittest module
    current_team: Union[None, Team]
        The current Team object or None if there isn't a team assigned yet
    default_move: list
        List of default move data required to create a Move object
    default_pokemon: list
        List of default pokemon data required to create a Pokemon object
    default_pokemon_list: list
        List of default team data required to create a Team object

    Methods:
    convert_to_objects(json_data: list)
        Converts the loaded json data into appropriate class objects for the application to use

    get_main_menu_options(self, mode: str)
        Gets the options to use in Data.main_menu_select()

    main_menu_select(self, mode: str)
        Displays the main menu

    new_team_name(self, current_team)
        Gets a new team name to create a new Team object or
        update the name attribute of the currently selected Team

    select_saved_team(self)
        Displays the input field for the user to select a saved team

    load_saved_team(self)
        Loads the team selected by the user in Data.select_saved_team()

    delete_saved_team(self)
        Deletes the team selected by the user in Data.select_saved_team()

    save_all_teams(self)
        Writes the contents of the team_data attribute to a .json file
    """

    def __init__(self, name: str) -> None:
        """
        Sets the required attributes for the Team object

        Parameters:
        name: str
            Name of the controller, either "main" for normal use or "test" for running the unittest module
        """

        self.current_team: Union[None, Team] = None
        self.default_move: list = ["None", 0, 0, 0, "None", 0, "None"]
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
        """
        Converts the loaded json data into appropriate class objects for the application to use

        Parameters:
        json_data: list
            The json data loaded from the .json file

        Returns:
        List containing the various class objects required by the application
        """

        converted_data: list = []
        for team in json_data:
            converted_data.append(Team.from_json(team))

        return converted_data

    def get_main_menu_options(self, mode: str) -> list:
        """
        Gets the options to use in Data.main_menu_select()

        Parameters:
        mode: str
            The currently running mode of the application

        Returns:
        List of menu options to display in Data.main_menu_select()
        """

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
        """
        Displays the main menu

        Parameters:
        mode: str
            The currently running mode of the application

        Returns:
        String of the user's input from the PyInquirer prompt
        """

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

    def new_team_name(self, current_team: Union[None, Team]) -> str:
        """
        Gets a new team name to create a new Team object or
        update the name attribute of the currently selected Team

        Parameters:
        current_team: Union[None, Team]
            The Team object saved to current_team or None

        Returns:
        Team name string input by the user into the PyInquirer prompt
        """

        current_name_list = [team.name for team in self.team_data] + [""]
        if current_team:
            try:
                current_name_list.remove(current_team.name)
            except ValueError:
                pass

        new_team_name: list = [
            {
                "type": "input",
                "name": "new_team_name",
                "message": "What would you like to name this team?:",
                "default": "New Team",
                "validate": lambda val: val.strip(" ") not in current_name_list or  # noqa: W504
                "Invalid name. Must contain at least 1 non-space character and not be in use by a currently saved team."
            }
        ]

        return prompt(new_team_name)["new_team_name"]

    def select_saved_team(self) -> str:
        """
        Displays the input field for the user to select a saved team

        Returns:
        String of the user's input from the PyInquirer prompt
        """

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
        """
        Loads the team selected by the user in Data.select_saved_team()

        Returns:
        None
        """

        selected_team: str = self.select_saved_team()

        for team in self.team_data:
            if team.name == selected_team:
                self.current_team = team

    def delete_saved_team(self) -> str:
        """
        Deletes the team selected by the user in Data.select_saved_team()

        Returns:
        None
        """

        selected_team: str = self.select_saved_team()

        for team in self.team_data:
            if team.name == selected_team:
                self.team_data.remove(team)
                self.current_team = None

        return f"{selected_team} has been deleted."

    def save_all_teams(self) -> tuple:
        """
        Writes the contents of the team_data attribute to a .json file

        Returns:
        Tuple containing a bool value of whether saving was successful and if unsuccessful, the error
        """

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
