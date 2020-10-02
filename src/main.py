#!/usr/bin/env python3

import os
import sys
import time
from typing import Union

import art  # type: ignore
import requests
import requests_cache  # type: ignore

from apihandler import APIHandler
from data import Data
from move import Move
from pokemon import Pokemon
from team import Team


def clear() -> None:
    """Clear screen utility function for both linux and windows"""
    if os.name == "nt":
        command = "cls"
    else:
        command = "clear"

    os.system(command)


def connection_error() -> None:
    """Print error messages and exit the application"""
    print("\n\n\n\u001b[7m !!! Pokéteams has encountered a connection issue !!! \u001b[0m\n\n")
    print("\u001b[1mYour current team data has been saved, please restart the app to continue from where you were interrupted.\u001b[0m")
    time.sleep(5)
    clear()
    exit()


def main(mode: str, message: str = "") -> None:
    """
    Main application function
    mode ("online" or "offline"), the mode that the application is currently running in
    message, the appropriate error message if there is a connection issue
    """
    deleted: str = ""

    while True:
        clear()
        print(art.text2art("Poketeams"))
        print("\u001b[1mBuild the ultimate Pokémon teams\u001b[0m\n\n")

        if message:
            print(f"\u001b[4m{message}\u001b[0m")
            print("\n\u001b[7m !!! Starting Pokéteams in offline mode !!! \u001b[0m\n")
            print("You will only be able to view, delete and rename saved teams while offline.")
            print("Please check your internet connection and restart the app to get full functionality.\n\n")

        team_controller: Data = Data("main")

        # Main menu screen
        if deleted != "":
            print(f"{deleted}\n")
            deleted == ""

        choice: str = team_controller.main_menu_select(mode)
        if choice == "Create a new team":
            name: str = team_controller.new_team_name(team_controller.current_team)
            team_controller.current_team = Team(name, team_controller.default_pokemon_list)
        elif choice == "Load a saved team":
            team_controller.load_saved_team()
        elif choice == "Delete a saved team":
            deleted = team_controller.delete_saved_team()
            team_controller.save_all_teams()
        else:
            team_controller.save_all_teams()
            clear()
            exit()

        current_team: Union[None, Team] = team_controller.current_team
        is_saved: tuple = (None, "")

        while current_team is not None:
            # View team screen
            clear()
            current_team.view_team()

            if is_saved[0] is True:
                print(f"\n{current_team.name} has been saved!\n")
                is_saved = (None, "")
            elif is_saved[0] is False:
                print(f"\nUnable to save {current_team.name}!")
                print(f"{is_saved[1]}\n")
                is_saved = (None, "")

            team_choice: str = current_team.team_menu(mode)

            if team_choice == "Save team":
                team_controller.team_data = current_team.team_save(team_controller.team_data)
                is_saved = team_controller.save_all_teams()
            elif team_choice == "Rename team":
                current_team.name = team_controller.new_team_name(current_team)
            elif team_choice == "Back to main menu":
                team_controller.team_data = current_team.team_save(team_controller.team_data)
                team_controller.save_all_teams()
                break
            else:
                current_pokemon: Pokemon = current_team.pokemon_list[int(team_choice) - 1]

                while True:
                    # View pokemon screen
                    clear()

                    # Only view information if there is an actual pokemon here otherwise skip to pokemon search/selection
                    if current_pokemon.name != "None":
                        current_pokemon.view_pokemon(current_team.name, team_choice)
                        pokemon_choice: str = current_pokemon.pokemon_menu(mode)
                    else:
                        pokemon_choice = "Change Pokémon"

                    if pokemon_choice == "Change Pokémon":
                        pokemon_lists: tuple = ("Generation 1", "Generation 2", "Generation 3", "Generation 4",
                                                "Generation 5", "Generation 6", "Generation 7", "Generation 8")
                        view_list: str = ""

                        while True:
                            # Search for pokemon screen
                            clear()

                            if view_list in pokemon_lists:
                                if view_list == "Generation 1":
                                    current_pokemon.view_pokemon_list(view_list, 1, api_handler.get_pokemon("", "?limit=151&offset=0"))
                                elif view_list == "Generation 2":
                                    current_pokemon.view_pokemon_list(view_list, 152, api_handler.get_pokemon("", "?limit=100&offset=151"))
                                elif view_list == "Generation 3":
                                    current_pokemon.view_pokemon_list(view_list, 252, api_handler.get_pokemon("", "?limit=135&offset=251"))
                                elif view_list == "Generation 4":
                                    current_pokemon.view_pokemon_list(view_list, 387, api_handler.get_pokemon("", "?limit=107&offset=386"))
                                elif view_list == "Generation 5":
                                    current_pokemon.view_pokemon_list(view_list, 494, api_handler.get_pokemon("", "?limit=156&offset=493"))
                                elif view_list == "Generation 6":
                                    current_pokemon.view_pokemon_list(view_list, 650, api_handler.get_pokemon("", "?limit=72&offset=649"))
                                elif view_list == "Generation 7":
                                    current_pokemon.view_pokemon_list(view_list, 722, api_handler.get_pokemon("", "?limit=88&offset=721"))
                                elif view_list == "Generation 8":
                                    current_pokemon.view_pokemon_list(view_list, 810, api_handler.get_pokemon("", "?limit=84&offset=809"))

                            try:
                                view_list = current_pokemon.select_pokemon(api_handler)
                            except Exception:
                                clear()
                                team_controller.team_data = current_team.team_save(team_controller.team_data)
                                team_controller.save_all_teams()
                                connection_error()

                            if view_list not in pokemon_lists:
                                # New pokemon view screen to confirm selection
                                # While it's unlikely for a connection issue to occur here if there was no error in the try/except block above
                                # include another to be safe as Pokemon.from_response() needs to make further api calls to get pokemon ability info
                                try:
                                    new_pokemon: Pokemon = Pokemon.from_response(api_handler, api_handler.get_pokemon(view_list))
                                except Exception:
                                    clear()
                                    team_controller.team_data = current_team.team_save(team_controller.team_data)
                                    team_controller.save_all_teams()
                                    connection_error()

                                clear()
                                new_pokemon.view_pokemon(current_team.name, team_choice)
                                confirm_pokemon: str = new_pokemon.confirm_pokemon()

                                if confirm_pokemon == "Add Pokémon":
                                    current_pokemon = new_pokemon
                                    current_team.pokemon_list[int(team_choice) - 1] = new_pokemon
                                    break

                    elif pokemon_choice == "Back to team view":
                        break
                    else:
                        current_move = current_pokemon.move_set[int(pokemon_choice) - 1]

                        while True:
                            # View move screen
                            clear()

                            # Only view information if there is a saved move here otherwise skip to move selection
                            if current_move.name != "None":
                                current_move.view_move(current_team.name, pokemon_choice, current_pokemon.name)
                                move_choice: str = current_move.move_menu(mode)
                            else:
                                move_choice = "Change move"

                            if move_choice == "Change move":
                                while True:
                                    # Move selection screen
                                    clear()
                                    current_move.view_move_list(current_pokemon.name, current_pokemon.move_list, current_pokemon.move_set)
                                    try:
                                        search_move: str = current_move.select_move(api_handler)
                                    except Exception:
                                        clear()
                                        team_controller.team_data = current_team.team_save(team_controller.team_data)
                                        team_controller.save_all_teams()
                                        connection_error()

                                    # New move view screen to confirm selection
                                    # Highly unlikely for a connection issue to occur here if there was no error in the try/except block above
                                    new_move: Move = Move.from_response(api_handler.get_move(search_move))

                                    clear()
                                    new_move.view_move(current_team.name, pokemon_choice, current_pokemon.name)
                                    confirm_move: str = new_move.confirm_move()

                                    if confirm_move == "Add move":
                                        current_move = new_move
                                        current_pokemon.move_set[int(pokemon_choice) - 1] = new_move
                                        break

                            if move_choice == "Back to Pokémon view":
                                break


if __name__ == "__main__":
    if "--help" in sys.argv:
        with open(os.path.dirname(os.path.abspath(__file__)) + "/help.md") as f:
            clear()
            print(f.read())
    else:
        # Check that we can connect to the api and start the app in the respective mode
        try:
            api_check: int = requests.get("https://pokeapi.co/api/v2/").status_code

            if api_check == 200:
                requests_cache.install_cache('pokeapi_cache')
                api_handler: APIHandler = APIHandler()
                main("online")
            else:
                message: str = "Pokeapi.co is currently unreachable."

        except requests.ConnectionError:
            message = "Your computer is not currently connected to the internet!"

        main("offline", message)
