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
            first_name = questionary.text("Enter the employee's first name:").ask()
            if first_name is None:
                continue
            
            first_name = first_name.strip().capitalize()
            
            if not first_name or not first_name.isalpha():
                print("Please enter a valid first name using letters only.")
                continue
            
            last_name = questionary.text("Enter the employee's last name:").ask()
            if last_name is None:
                continue
            
            last_name = last_name.strip().capitalize()
            
            if not last_name or not last_name.isalpha():
                print("Please enter a valid last name using letters only.")
                continue
            
            # Generate email automatically
            email = f"{first_name.lower()}{last_name.lower()}@respawnpoint.com"
            
            # Check for duplicates
            full_name = f"{first_name} {last_name}"
            if any(emp["first_name"].casefold() == first_name.casefold() and emp["last_name"].casefold() == last_name.casefold() for emp in employees):
                print(f"{full_name} is already in the employee list.")
            else:
                new_employee = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email
                }
                employees.append(new_employee)
                save_employees(employees)
                print(f"{full_name} has been added to the employee list.")
                print(f"Email: {email}")

        elif admin_answer == "Remove Employee":
            if not employees:
                print("No employees to remove.")
                continue
            
            # Create employee name display options
            employee_names = [f"{emp['first_name']} {emp['last_name']}" for emp in employees]
            menu_choices = employee_names + ["Search Employees", "Back"]
            
            selected_option = questionary.select(
                "Remove Employee Menu:",
                choices=menu_choices
            ).ask()
            
            if selected_option == "Search Employees":
                emp_to_remove = questionary.autocomplete(
                    "Search for an employee to remove:",
                    choices=employee_names
                ).ask()
            else:
                emp_to_remove = selected_option if selected_option in employee_names else None
            
            if emp_to_remove:
                # Find and remove the employee
                employees = [emp for emp in employees if f"{emp['first_name']} {emp['last_name']}" != emp_to_remove]
                save_employees(employees)
                print(f"{emp_to_remove} has been removed from the employee list.")

        elif admin_answer == "Edit Employee":
            if not employees:
                print("No employees to edit.")
                continue
            
            # Create employee name display options
            employee_names = [f"{emp['first_name']} {emp['last_name']}" for emp in employees]
            menu_choices = employee_names + ["Search Employees", "Back"]
            
            selected_option = questionary.select(
                "Edit Employee Menu:",
                choices=menu_choices
            ).ask()
            
            if selected_option == "Search Employees":
                emp_to_edit = questionary.autocomplete(
                    "Search for an employee to edit:",
                    choices=employee_names
                ).ask()
            else:
                emp_to_edit = selected_option if selected_option in employee_names else None
            
            if emp_to_edit:
                # Find the employee
                emp_index = next((i for i, emp in enumerate(employees) if f"{emp['first_name']} {emp['last_name']}" == emp_to_edit), None)
                
                if emp_index is not None:
                    what_to_change = questionary.select(
                        f"What would you like to change for {emp_to_edit}?",
                        choices=["First Name", "Last Name", "Back"]
                    ).ask()
                    
                    if what_to_change == "First Name":
                        new_first_name = questionary.text(f"Enter new first name (current: {employees[emp_index]['first_name']}):").ask()
                        if new_first_name and new_first_name.strip().isalpha():
                            employees[emp_index]["first_name"] = new_first_name.strip().capitalize()
                            # Update email
                            employees[emp_index]["email"] = f"{employees[emp_index]['first_name'].lower()}{employees[emp_index]['last_name'].lower()}@respawnpoint.com"
                            save_employees(employees)
                            print(f"First name updated!")
                    
                    elif what_to_change == "Last Name":
                        new_last_name = questionary.text(f"Enter new last name (current: {employees[emp_index]['last_name']}):").ask()
                        if new_last_name and new_last_name.strip().isalpha():
                            employees[emp_index]["last_name"] = new_last_name.strip().capitalize()
                            # Update email
                            employees[emp_index]["email"] = f"{employees[emp_index]['first_name'].lower()}{employees[emp_index]['last_name'].lower()}@respawnpoint.com"
                            save_employees(employees)
                            print(f"Last name updated!")

        elif admin_answer == "View Employees":
            employees = load_employees()
            if not employees:
                print("No employees found.")
            else:
                print("\n--- Current Employees ---")
                for emp in employees:
                    print(f"Name: {emp['first_name']} {emp['last_name']}")
                    print(f"Email: {emp['email']}")
                    print()
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
                # Get list of game titles and separate by stock status
                game_titles = os.listdir(games_dir)
                available_games = []
                out_of_stock_games = []
                
                for game_title in game_titles:
                    game_path = os.path.join(games_dir, game_title, "game_info.json")
                    if os.path.exists(game_path):
                        with open(game_path, "r") as f:
                            game_data = json.load(f)
                            stock = game_data.get('stock', 0)
                            if stock > 0:
                                available_games.append(game_title)
                            else:
                                out_of_stock_games.append(game_title)
                
                # Display available and out of stock games
                print("\n--- Available Games ---")
                for game in available_games:
                    game_path = os.path.join(games_dir, game, "game_info.json")
                    with open(game_path, "r") as f:
                        game_data = json.load(f)
                        stock = game_data.get('stock', 0)
                    print(f"• {game} (Stock: {stock})")
                
                if out_of_stock_games:
                    print("\n--- Out of Stock ---")
                    for game in out_of_stock_games:
                        print(f"• {game} (Stock: 0)")
                
                print()
                
                # Create menu choices
                all_games = available_games + out_of_stock_games
                menu_choices = all_games + ["Search Games", "Back"]
                
                # Show view games menu with game titles as selectable options
                selected_option = questionary.select(
                    "Games Menu:",
                    choices=menu_choices
                ).ask()
                
                if selected_option == "Search Games":
                    # Let user search and select a game
                    selected_game = questionary.autocomplete(
                        "Search for a game to view details:",
                        choices=all_games
                    ).ask()
                    
                    if selected_game is not None:
                        game_path = os.path.join(games_dir, selected_game, "game_info.json")
                        if os.path.exists(game_path):
                            with open(game_path, "r") as f:
                                game_data = json.load(f)
                                print(f"\nTitle: {selected_game}")
                                print(f"Price: €{game_data.get('price', 'N/A')}")
                                print(f"Stock: {game_data.get('stock', 0)}")
                                print("Synopsis:")
                                print(f"  {game_data.get('synopsis', 'N/A')}")
                                print()
                                wait = questionary.text("Press Enter to return to the Employee panel.").ask()
                
                elif selected_option and selected_option in all_games:
                    # If a game title was selected directly
                    game_path = os.path.join(games_dir, selected_option, "game_info.json")
                    if os.path.exists(game_path):
                        with open(game_path, "r") as f:
                            game_data = json.load(f)
                            print(f"\nTitle: {selected_option}")
                            print(f"Price: €{game_data.get('price', 'N/A')}")
                            print(f"Stock: {game_data.get('stock', 0)}")
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
            
            game_stock = questionary.text("How many copies in stock?").ask()
            if game_stock is None:
                continue
            
            game_stock = game_stock.strip()
            if not game_stock.isdigit():
                print("Please enter a valid number for stock.")
                continue
            
            game_stock = int(game_stock)
            
            # Create games directory if it doesn't exist
            games_dir = os.path.join("games", game_name)
            os.makedirs(games_dir, exist_ok=True)
            
            # Create JSON file with title, price, synopsis, and stock
            game_data = {
                "title": game_name,
                "price": game_price,
                "synopsis": game_synopsis,
                "stock": game_stock
            }
            game_file = os.path.join(games_dir, "game_info.json")
            
            with open(game_file, "w") as f:
                json.dump(game_data, f, indent=4)
            
            print(f"'{game_name}' has been added successfully with {game_stock} copies in stock!")

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
                        choices=["Title", "Price", "Synopsis", "Stock", "Back"]
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
                        
                        elif what_to_change == "Stock":
                            new_stock = questionary.text(f"Enter new stock (current: {game_data.get('stock', 0)}):").ask()
                            if new_stock and new_stock.strip().isdigit():
                                game_data["stock"] = int(new_stock.strip())
                                with open(game_path, "w") as f:
                                    json.dump(game_data, f, indent=4)
                                print(f"Stock updated to {new_stock.strip()}!")
                        
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