#!/usr/bin/env python3

import os
import sys

import art  # type: ignore
import requests
import requests_cache  # type: ignore

from apihandler import APIHandler
from data import Data
from pokemon import Pokemon
# from team import Team
# import json


def clear():
    if os.name == "nt":
        command = "cls"
    else:
        command = "clear"

    os.system(command)


def main_online():
    while True:
        clear()
        print(art.text2art("Poketeams"))
        print("Build the ultimate pokemon teams\n\n")
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
            clear()
            exit()

        current_team = team_controller.current_team
        is_saved = (None, "")
        while current_team is not None:
            clear()
            current_team.view_team()
            if is_saved[0] is True:
                print(f"\n{current_team.name} has been saved!\n")
                is_saved = (None, "")
            elif is_saved[0] is False:
                print(f"\nUnable to save {current_team.name}!")
                print(f"{is_saved[1]}\n")
                is_saved = (None, "")
            team_choice = current_team.team_menu()
            if team_choice == "Save team":
                team_controller.team_data = current_team.team_save(team_controller.team_data)
                is_saved = team_controller.save_all_teams()
            elif team_choice == "Back to main menu":
                team_controller.team_data = current_team.team_save(team_controller.team_data)
                team_controller.save_all_teams()
                break
            else:
                current_pokemon = current_team.pokemon_list[team_choice]
                while True:
                    clear()
                    current_pokemon.view_pokemon(current_team.name, team_choice)
                    pokemon_choice = current_pokemon.pokemon_menu()
                    if pokemon_choice == "Change Pokemon":
                        pass
                        pokemon_lists = ("Generation 1", "Generation 2",
                                         "Generation 3", "Generation 4",
                                         "Generation 5", "Generation 6",
                                         "Generation 7", "Generation 8")
                        view_list = ""
                        while True:
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
                            view_list = current_pokemon.select_pokemon(api_handler)
                            if view_list not in pokemon_lists:
                                response = api_handler.get_pokemon(view_list)
                                new_pokemon = Pokemon.from_response(api_handler, response)
                                clear()
                                new_pokemon.view_pokemon(current_team.name, team_choice)
                                confirm_pokemon = new_pokemon.confirm_pokemon()
                                if confirm_pokemon == "Add Pokémon":
                                    current_pokemon = new_pokemon
                                    current_team.pokemon_list[team_choice] = new_pokemon
                                    break
                    elif pokemon_choice == "Back to team view":
                        break
                    else:
                        pass
                        # current_move = current_pokemon.move_set[pokemon_choice]
                        # current_move.view_move()
                        # move_choice =  current_move.move_menu()
                        # if move_choice = "Change move":
                        #     while True:
                        #         current_pokemon.view_move_list()
                        #         search_move = current_move.select_move()
                        #         r = apihandler.get_move(search_move)
                        #         new_move = Move(respone data)
                        #         new_move.view_move()
                        #         confirm_move = new_move.confirm_move()
                        #         if confirm_move is True:
                        #             current_move = new_move
                        #             current_pokemon.move_set[pokemon_choice] = new_move
                        #             break


if __name__ == "__main__":
    if "--help" in sys.argv:
        with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/help.md") as f:
            print(f.read())
    else:
        try:
            api_check = requests.get("https://pokeapi.co/api/v2/").status_code
            if api_check == 200:
                requests_cache.install_cache('pokeapi_cache')
                api_handler = APIHandler()
                team_controller = Data("main")
                main_online()
            else:
                message = "Pokeapi.co is currently unreachable."
        except requests.ConnectionError:
            message = "Your computer is not currently connected to the internet!"

# this is to get test data for testing save function
# team = Team("test team", team_controller.default_pokemon_list)
# print(json.dumps(team, default=lambda o: o.__dict__))

# Additional feature if time, have offline mode to only view saved teams
