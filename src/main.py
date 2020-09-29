import os

import art
import requests
import requests_cache

from apihandler import APIHandler
from data import Data


def clear():
    if os.name == "nt":
        command = "cls"
    else:
        command = "clear"

    os.system(command)


requests_cache.install_cache('pokeapi_cache')
api_handler = APIHandler()
team_controller = Data("main")

# __name__ ==
# add -help flag
# Additional feature if time, have offline mode to only view saved teams
# try/except to catch error with no internet connection
# if/else to check response status code
# with requests_cache.disabled():
    # requests.get("https://pokeapi.co/api/v2/")

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
            team_controller.team_data = current_team.team_save(
                                        team_controller.team_data)
            is_saved = team_controller.save_all_teams()
        elif team_choice == "Back to main menu":
            team_controller.team_data = current_team.team_save(
                                        team_controller.team_data)
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
                    # pokemon_lists = ()
                    # view_list = ""
                    # while True:
                        # if view_list in pokemon_lists:
                            # current_pokemon.view_pokemon_list(view_list)
                            # view_list = ""
                        # view_list = current_pokemon.select_pokemon()
                        # if view_list not in pokemon_lists:
                            # r = apihandler.get_pokemon(view_list)
                            # new_pokemon = Pokemon(response data)
                            # new_pokemon.view_pokemon()
                            # confirm_pokemon = new_pokemon.confirm_pokemon()
                            # if confirm_pokemon is True:
                                # current_pokemon = new_pokemon
                                # current_team.pokemon_list[team_choice] = new_pokemon
                                # break
                            # else:
                                # view_list = ""               
                elif pokemon_choice == "Back to team view":
                    break
                else:
                    current_move = current_pokemon.move_set[pokemon_choice]
                    # current_move.view_move()
                    # move_choice =  current_move.move_menu()
                    # if move_choice = "Change move":
                        # while True:
                            # current_pokemon.view_move_list()
                            # search_move = current_move.select_move()
                            # r = apihandler.get_move(search_move)
                            # new_move = Move(respone data)
                            # new_move.view_move()
                            # confirm_move = new_move.confirm_move()
                            # if confirm_move is True:
                                # current_move = new_move
                                # current_pokemon.move_set[pokemon_choice] = new_move
                                # break
