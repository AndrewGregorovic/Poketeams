import os
import requests_cache
from data import Data
from apihandler import APIHandler
import art


def clear():
    if os.name == "nt":
        command = "cls"
    else:
        command = "clear"

    os.system(command)


requests_cache.install_cache('pokeapi_cache')
api_handler = APIHandler()
team_controller = Data()

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
            clear()
            current_pokemon = current_team.pokemon_list[team_choice]
            current_pokemon.view_pokemon(current_team.name, team_choice)
            pokemon_choice = current_pokemon.pokemon_menu()
            if pokemon_choice == "Change Pokemon":
                print("Pokemon selection here")
            elif pokemon_choice == "Back to team view":
                print("Back to team view here")
            else:
                print("View move here")
