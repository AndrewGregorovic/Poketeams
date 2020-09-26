import requests_cache
from data import Data
from apihandler import APIHandler


print("Poketeams")
print("Build your pokemon dream teams")
requests_cache.install_cache('pokeapi_cache')
api_handler = APIHandler()
team_controller = Data()

while True:
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
        exit()

    current_team = team_controller.current_team
    while current_team != None:
        current_team.view_team()
        team_choice = current_team.team_menu()
        if team_choice == "Save team":
            team_controller.team_data = current_team.team_save(team_controller.team_data)
            team_controller.save_all_teams()
        elif team_choice == "Back to main menu":
            team_controller.team_data = current_team.team_save(team_controller.team_data)
            team_controller.save_all_teams()
            break
        else:
            current_pokemon = current_team.pokemon_list[team_choice]
            current_pokemon.view_pokemon(current_team.name, team_choice)
            pokemon_choice = current_pokemon.pokemon_menu()
            if pokemon_choice == "Change Pokemon":
                print("Pokemon selection here")
            elif pokemon_choice == "Back to team view":
                print("Back to team view here")
            else:
                print("View move here")