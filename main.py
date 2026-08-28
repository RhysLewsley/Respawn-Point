import json
import os
import shutil
import questionary
import game_list

json_file = "employee_list.json"


def load_employees():
    """loads employee list from the JSON file."""
    if not os.path.exists(json_file):
        return []
    try:
        with open(json_file, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []  

def save_employees(employees):
    """Saves the employee list back to the JSON file."""
    with open(json_file, "w") as f:
        json.dump(employees, f, indent=4)


while True:
    exit_app = False
    answer = questionary.select(
        "Welcome to the Respawn Point app! Please select an option below:",
        choices=["Admin", "Employee", "Customer", "Exit App"],
    ).ask()

    if answer == "Exit App":
        print("Goodbye!")
        break

    # Admin Panel
    while answer == "Admin":
        employees = load_employees()
        admin_answer = questionary.select(
            "Welcome to the Admin panel! Please select an option below:",
            choices=[
                "Add Employee",
                "Remove Employee",
                "Edit Employee",
                "View Employees",
                "Exit",
            ],
        ).ask()

        if admin_answer == "Add Employee":
            new_emp_input = questionary.text("Enter the name of the new employee:").ask()

            if new_emp_input is None:
                continue

            new_emp = new_emp_input.strip()

            if not new_emp:
                print("Please enter a name.")
                continue

            # Reject any character that is not a letter or a space.
            if any(not (char.isalpha() or char.isspace()) for char in new_emp):
                print("Sorry that's not a valid name. Please type a name using letters only.")
                continue

            new_emp = " ".join(part.capitalize() for part in new_emp.split())

            # 2. Next, check for duplicates
            if any(emp.casefold() == new_emp.casefold() for emp in employees):
                print(f"{new_emp} is already in the employee list.")

            # 3. If it passes both checks, it is a valid, unique name
            else:
                employees.append(new_emp)
                save_employees(employees)
                print(f"{new_emp} has been added to the employee list.")

        elif admin_answer == "Remove Employee":
            if not employees:
                print("No employees to remove.")
                continue

            emp_to_remove = questionary.select(
                "Select an employee to remove:", choices=employees
            ).ask()

            if emp_to_remove is None:
                continue

            employees.remove(emp_to_remove)
            save_employees(employees)
            print(f"{emp_to_remove} has been removed from the employee list.")

        elif admin_answer == "Edit Employee":
            if not employees:
                print("No employees to edit.")
                continue

            emp_to_edit = questionary.select(
                "Select an employee to edit:", choices=employees
            ).ask()

            if emp_to_edit is None:
                continue

            new_name = questionary.text(f"Enter the new name for {emp_to_edit}:").ask()

            if new_name is None:
                continue

            new_name = new_name.strip()

            if not new_name:
                print("Please enter a name.")
                continue

            # Reject any character that is not a letter or a space.
            if any(not (char.isalpha() or char.isspace()) for char in new_name):
                print("Sorry that's not a valid name. Please type a name using letters only.")
                continue

            new_name = " ".join(part.capitalize() for part in new_name.split())

            # 2. Next, check for duplicates
            if any(emp.casefold() == new_name.casefold() for emp in employees):
                print(f"{new_name} is already in the employee list.")

            # 3. If it passes both checks, it is a valid, unique name
            else:
                employees.remove(emp_to_edit)
                employees.append(new_name)
                save_employees(employees)
                print(f"{emp_to_edit} has been edited to {new_name}.")

        elif admin_answer == "View Employees":
            employees = load_employees()
            if not employees:
                print("No employees found.")
            else:
                print("\nCurrent Employees:")
                for emp in employees:
                    print(f"- {emp}")
                print()  # Add an extra newline for spacing
                wait_for_input = questionary.text("Press Enter to return to the Admin panel.").ask()
        elif admin_answer == "Exit":
            print("Goodbye!")
            exit_app = True
            break

    #if exit_app:
       #break

    while answer == "Employee":
        employee_panel = questionary.select(
            "Welcome to the Employee panel! Please select an option below:",
            choices=[
                "View Games",
                "View Discounts",
                "Add Game",
                "Edit Game",
                "Delete Game",
                "Exit"
            ],
            ).ask()
        if employee_panel == "View Games":
            games_dir = "games"
            if not os.path.exists(games_dir) or not os.listdir(games_dir):
                print("No games found.")
            else:
                # Get list of game titles
                game_titles = os.listdir(games_dir)
                
                # Create menu choices with game titles + options
                menu_choices = game_titles + ["Search Games", "Back"]
                
                # Show view games menu with game titles as selectable options
                selected_option = questionary.select(
                    "Games Menu:",
                    choices=menu_choices
                ).ask()
                
                if selected_option == "Search Games":
                    # Let user search and select a game
                    selected_game = questionary.autocomplete(
                        "Search for a game to view details:",
                        choices=game_titles
                    ).ask()
                    
                    if selected_game is not None:
                        game_path = os.path.join(games_dir, selected_game, "game_info.json")
                        if os.path.exists(game_path):
                            with open(game_path, "r") as f:
                                game_data = json.load(f)
                                print(f"\nTitle: {selected_game}")
                                print(f"Price: €{game_data.get('price', 'N/A')}")
                                print("Synopsis:")
                                print(f"{game_data.get('synopsis', 'N/A')}")
                                print()
                                wait = questionary.text("Press Enter to return to the Employee panel.").ask()
                
                elif selected_option and selected_option in game_titles:
                    # If a game title was selected directly
                    game_path = os.path.join(games_dir, selected_option, "game_info.json")
                    if os.path.exists(game_path):
                        with open(game_path, "r") as f:
                            game_data = json.load(f)
                            print(f"\nTitle: {selected_option}")
                            print(f"Price: €{game_data.get('price', 'N/A')}")
                            print("Synopsis:")
                            print(f"  {game_data.get('synopsis', 'N/A')}")
                            print()
                            wait = questionary.text("Press Enter to return to the Employee panel.").ask()

        elif employee_panel == "View Discounts":
            print("view Discount")

        elif employee_panel == "Add Game":
            game_name = questionary.text("What is the game's title?").ask()
            if game_name is None:
                continue
            
            game_name = game_name.strip().title()
            
            game_price = questionary.text("What is the price of the game?").ask()
            if game_price is None:
                continue
            
            game_price = game_price.strip()
            
            game_synopsis = questionary.text("Please provide a brief synopsis:").ask()
            if game_synopsis is None:
                continue
            
            game_synopsis = game_synopsis.strip()
            
            # Create games directory if it doesn't exist
            games_dir = os.path.join("games", game_name)
            os.makedirs(games_dir, exist_ok=True)
            
            # Create JSON file with title, price, and synopsis
            game_data = {
                "title": game_name,
                "price": game_price,
                "synopsis": game_synopsis
            }
            game_file = os.path.join(games_dir, "game_info.json")
            
            with open(game_file, "w") as f:
                json.dump(game_data, f, indent=4)
            
            print(f"'{game_name}' has been added successfully!")

        elif employee_panel == "Edit Game":
            games_dir = "games"
            if not os.path.exists(games_dir) or not os.listdir(games_dir):
                print("No games to edit.")
                continue
            else:
                # Get list of game titles
                game_titles = os.listdir(games_dir)
                
                # Create menu choices with game titles + options
                menu_choices = game_titles + ["Search Games", "Back"]
                
                # Show edit games menu with game titles as selectable options
                selected_option = questionary.select(
                    "Edit Game Menu:",
                    choices=menu_choices
                ).ask()
                
                if selected_option == "Search Games":
                    # Let user search and select a game
                    selected_game = questionary.autocomplete(
                        "Search for a game to edit:",
                        choices=game_titles
                    ).ask()
                else:
                    selected_game = selected_option if selected_option in game_titles else None
                
                if selected_game:
                    # Ask what to change
                    what_to_change = questionary.select(
                        f"What would you like to change for '{selected_game}'?",
                        choices=["Title", "Price", "Synopsis", "Back"]
                    ).ask()
                    
                    game_path = os.path.join(games_dir, selected_game, "game_info.json")
                    if os.path.exists(game_path):
                        with open(game_path, "r") as f:
                            game_data = json.load(f)
                        
                        if what_to_change == "Title":
                            new_title = questionary.text(f"Enter new title (current: {selected_game}):").ask()
                            if new_title and new_title.strip():
                                new_title = new_title.strip().title()
                                game_data["title"] = new_title
                                # Rename the directory
                                new_game_path = os.path.join(games_dir, new_title)
                                os.rename(os.path.join(games_dir, selected_game), new_game_path)
                                # Save with new path
                                with open(os.path.join(new_game_path, "game_info.json"), "w") as f:
                                    json.dump(game_data, f, indent=4)
                                print(f"Game title updated to '{new_title}'!")
                        
                        elif what_to_change == "Price":
                            new_price = questionary.text(f"Enter new price (current: {game_data.get('price', 'N/A')}):").ask()
                            if new_price and new_price.strip():
                                game_data["price"] = new_price.strip()
                                with open(game_path, "w") as f:
                                    json.dump(game_data, f, indent=4)
                                print(f"Price updated to €{new_price.strip()}!")
                        
                        elif what_to_change == "Synopsis":
                            new_synopsis = questionary.text(f"Enter new synopsis:").ask()
                            if new_synopsis and new_synopsis.strip():
                                game_data["synopsis"] = new_synopsis.strip()
                                with open(game_path, "w") as f:
                                    json.dump(game_data, f, indent=4)
                                print(f"Synopsis updated!")
                        
                        if what_to_change != "Back":
                            wait = questionary.text("Press Enter to return to the Employee panel.").ask()

        elif employee_panel == "Delete Game":
            games_dir = "games"
            if not os.path.exists(games_dir) or not os.listdir(games_dir):
                print("No games to delete.")
                continue
            
            # Get list of game folders
            available_games = os.listdir(games_dir)
            
            # Create menu choices with game titles + options
            menu_choices = available_games + ["Search Games", "Back"]
            
            # Display selection
            selected_option = questionary.select(
                "Delete Game Menu:",
                choices=menu_choices
            ).ask()
            
            if selected_option == "Search Games":
                # Let user search and select a game
                game_to_delete = questionary.autocomplete(
                    "Search for a game to delete:",
                    choices=available_games
                ).ask()
            else:
                game_to_delete = selected_option if selected_option in available_games else None
            
            if game_to_delete:
                # Delete the game folder
                game_path = os.path.join(games_dir, game_to_delete)
                shutil.rmtree(game_path)
                print(f"'{game_to_delete}' has been deleted successfully!")   

        elif employee_panel == "Exit":
                print("Goodbye!")
                exit_app = True
                break


    if exit_app:
        break