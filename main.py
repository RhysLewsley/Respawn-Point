import json
import os
import shutil
import questionary
import game_list

json_file = "employee_list.json"
discounts_file = "discounts.json"


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


def load_discounts():
    """Loads discount list from the JSON file."""
    if not os.path.exists(discounts_file):
        return []
    try:
        with open(discounts_file, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_discounts(discounts):
    """Saves the discount list back to the JSON file."""
    with open(discounts_file, "w") as f:
        json.dump(discounts, f, indent=4)


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
                "Add Discount",
                "Edit Discount",
                "Delete Discount",
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
        
        elif admin_answer == "Add Discount":
            discounts = load_discounts()
            discount_name = questionary.text("Enter discount name (e.g., 'Spring Sale'):").ask()
            if discount_name is None:
                continue
            
            discount_name = discount_name.strip()
            
            if not discount_name:
                print("Please enter a valid discount name.")
                continue
            
            discount_code = questionary.text("Enter discount code (e.g., 'SPRING20'):").ask()
            if discount_code is None:
                continue
            
            discount_code = discount_code.strip().upper()
            
            if not discount_code:
                print("Please enter a valid discount code.")
                continue
            
            # Check for duplicate codes
            if any(disc["code"].upper() == discount_code for disc in discounts):
                print(f"Discount code '{discount_code}' already exists.")
                continue
            
            discount_value = questionary.text("Enter discount percentage (e.g., '20' for 20%):").ask()
            if discount_value is None:
                continue
            
            try:
                discount_value = float(discount_value)
                if discount_value < 0 or discount_value > 100:
                    print("Please enter a value between 0 and 100.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue
            
            # Select games for the discount
            games_dir = "games"
            game_titles = []
            if os.path.exists(games_dir):
                game_titles = os.listdir(games_dir)
            
            if not game_titles:
                print("No games available to apply discount to.")
                continue
            
            selected_games = questionary.checkbox(
                "Select games to apply this discount to:",
                choices=game_titles
            ).ask()
            
            if selected_games is None:
                continue
            
            if not selected_games:
                print("Please select at least one game.")
                continue
            
            new_discount = {
                "name": discount_name,
                "code": discount_code,
                "percentage": discount_value,
                "games": selected_games
            }
            discounts.append(new_discount)
            save_discounts(discounts)
            print(f"Discount '{discount_name}' with code '{discount_code}' ({discount_value}%) has been added to {len(selected_games)} game(s).")
        
        elif admin_answer == "Edit Discount":
            discounts = load_discounts()
            if not discounts:
                print("No discounts to edit.")
                continue
            
            discount_codes = [f"{disc['code']} - {disc['name']} ({disc['percentage']}%) - Games: {', '.join(disc.get('games', []))}" for disc in discounts]
            menu_choices = discount_codes + ["Back"]
            
            selected_option = questionary.select(
                "Edit Discount Menu:",
                choices=menu_choices
            ).ask()
            
            if selected_option and selected_option != "Back":
                # Extract discount code from the choice
                discount_code = selected_option.split(" - ")[0]
                
                # Find the discount
                disc_index = next((i for i, disc in enumerate(discounts) if disc['code'] == discount_code), None)
                
                if disc_index is not None:
                    what_to_change = questionary.select(
                        f"What would you like to change for {discount_code}?",
                        choices=["Name", "Code", "Percentage", "Games", "Back"]
                    ).ask()
                    
                    if what_to_change == "Name":
                        new_name = questionary.text(f"Enter new name (current: {discounts[disc_index]['name']}):").ask()
                        if new_name and new_name.strip():
                            discounts[disc_index]["name"] = new_name.strip()
                            save_discounts(discounts)
                            print("Discount name updated!")
                    
                    elif what_to_change == "Code":
                        new_code = questionary.text(f"Enter new code (current: {discounts[disc_index]['code']}):").ask()
                        if new_code and new_code.strip():
                            new_code = new_code.strip().upper()
                            if any(disc["code"].upper() == new_code and i != disc_index for i, disc in enumerate(discounts)):
                                print(f"Code '{new_code}' already exists.")
                            else:
                                discounts[disc_index]["code"] = new_code
                                save_discounts(discounts)
                                print("Discount code updated!")
                    
                    elif what_to_change == "Percentage":
                        new_percentage = questionary.text(f"Enter new percentage (current: {discounts[disc_index]['percentage']}%):").ask()
                        if new_percentage:
                            try:
                                new_percentage = float(new_percentage)
                                if 0 <= new_percentage <= 100:
                                    discounts[disc_index]["percentage"] = new_percentage
                                    save_discounts(discounts)
                                    print("Discount percentage updated!")
                                else:
                                    print("Please enter a value between 0 and 100.")
                            except ValueError:
                                print("Please enter a valid number.")
                    
                    elif what_to_change == "Games":
                        games_action = questionary.select(
                            "What would you like to do?",
                            choices=["Add Game", "Remove Game", "Back"]
                        ).ask()
                        
                        if games_action == "Add Game":
                            games_dir = "games"
                            game_titles = []
                            if os.path.exists(games_dir):
                                game_titles = os.listdir(games_dir)
                            
                            if not game_titles:
                                print("No games available.")
                            else:
                                current_games = discounts[disc_index].get('games', [])
                                available_games = [game for game in game_titles if game not in current_games]
                                
                                if not available_games:
                                    print("No games available to add.")
                                else:
                                    game_to_add = questionary.select(
                                        "Select a game to add to this discount:",
                                        choices=available_games + ["Back"]
                                    ).ask()
                                    
                                    if game_to_add and game_to_add != "Back":
                                        discounts[disc_index]["games"].append(game_to_add)
                                        save_discounts(discounts)
                                        print(f"Added '{game_to_add}' to the discount!")
                        
                        elif games_action == "Remove Game":
                            current_games = discounts[disc_index].get('games', [])
                            
                            if not current_games:
                                print("No games to remove from this discount.")
                            else:
                                game_to_remove = questionary.select(
                                    "Select a game to remove from this discount:",
                                    choices=current_games + ["Back"]
                                ).ask()
                                
                                if game_to_remove and game_to_remove != "Back":
                                    discounts[disc_index]["games"].remove(game_to_remove)
                                    save_discounts(discounts)
                                    print(f"Removed '{game_to_remove}' from the discount!")
        
        elif admin_answer == "Delete Discount":
            discounts = load_discounts()
            if not discounts:
                print("No discounts to delete.")
                continue
            
            discount_codes = [f"{disc['code']} - {disc['name']} ({disc['percentage']}%) - Games: {', '.join(disc.get('games', []))}" for disc in discounts]
            menu_choices = discount_codes + ["Back"]
            
            selected_option = questionary.select(
                "Delete Discount Menu:",
                choices=menu_choices
            ).ask()
            
            if selected_option and selected_option != "Back":
                # Extract discount code from the choice
                discount_code = selected_option.split(" - ")[0]
                
                # Find and remove the discount
                discounts = [disc for disc in discounts if disc['code'] != discount_code]
                save_discounts(discounts)
                print(f"Discount '{discount_code}' has been deleted.")
        
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
            discounts = load_discounts()
            if not discounts:
                print("\nNo discounts available.")
            else:
                print("\n--- Active Discounts ---")
                for disc in discounts:
                    games_list = ", ".join(disc.get('games', []))
                    print(f"\nCode: {disc['code']}")
                    print(f"Name: {disc['name']}")
                    print(f"Discount: {disc['percentage']}%")
                    print(f"Applies to: {games_list}")
            wait = questionary.text("\nPress Enter to return to the Employee panel.").ask()

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

    while answer == "Customer":
        # Initialize customer basket for this session
        if 'customer_basket' not in locals():
            customer_basket = []
        
        customer_panel = questionary.select(
            "Welcome (customer name or guest), Please select an option below:",
            choices=[
                "Browse Games",
                "Search for Game",
                "View Basket",
                "View Discounts",
                "Exit"
            ],
        ).ask()

        if customer_panel == "Browse Games":
            games_dir = "games"
            if not os.path.exists(games_dir) or not os.listdir(games_dir):
                print("No games available at the moment.")
            else:
                # Get list of all game titles
                game_titles = os.listdir(games_dir)
                all_games = {}
                
                for game_title in game_titles:
                    game_path = os.path.join(games_dir, game_title, "game_info.json")
                    if os.path.exists(game_path):
                        with open(game_path, "r") as f:
                            game_data = json.load(f)
                            stock = game_data.get('stock', 0)
                            all_games[game_title] = {
                                'price': game_data.get('price', 'N/A'),
                                'stock': stock,
                                'synopsis': game_data.get('synopsis', 'N/A')
                            }
                
                if not all_games:
                    print("No games at the moment.")
                else:
                    # Create menu choices with formatted game info
                    menu_choices = []
                    for game_title, game_info in all_games.items():
                        price = game_info['price']
                        status = "available" if game_info['stock'] > 0 else "out of stock"
                        formatted_choice = f"{game_title} - €{price} {status}"
                        menu_choices.append(formatted_choice)
                    
                    menu_choices.append("Back")
                    
                    # Show browse games menu
                    selected_option = questionary.select(
                        "Select a game to view details:",
                        choices=menu_choices
                    ).ask()
                    
                    if selected_option and selected_option != "Back":
                        # Extract game title from formatted choice
                        game_title = selected_option.split(" - €")[0]
                        if game_title in all_games:
                            # Display game details
                            game_info = all_games[game_title]
                            status = "available" if game_info['stock'] > 0 else "out of stock"
                            print(f"\n--- {game_title} ---")
                            print(f"Price: €{game_info['price']}")
                            print(f"Status: {status}")
                            print(f"Synopsis:")
                            print(f"  {game_info['synopsis']}")
                            print()
                            
                            # Show Buy/Add to Basket/Back menu
                            buy_menu = questionary.select(
                                "What would you like to do?",
                                choices=["Buy", "Add to Basket", "Back"]
                            ).ask()
                            
                            if buy_menu == "Buy":
                                if game_info['stock'] > 0:
                                    # Check for applicable discount (find the biggest one)
                                    discounts = load_discounts()
                                    final_price = game_info['price']
                                    discount_applied = None
                                    
                                    # Find all applicable discounts and select the biggest one
                                    applicable_discounts = [disc for disc in discounts if game_title in disc.get('games', [])]
                                    if applicable_discounts:
                                        discount_applied = max(applicable_discounts, key=lambda x: x['percentage'])
                                        discount_amount = final_price * (discount_applied['percentage'] / 100)
                                        final_price = final_price - discount_amount
                                    
                                    # Reduce stock by 1
                                    game_path = os.path.join(games_dir, game_title, "game_info.json")
                                    with open(game_path, "r") as f:
                                        game_data = json.load(f)
                                    game_data['stock'] = game_data.get('stock', 0) - 1
                                    with open(game_path, "w") as f:
                                        json.dump(game_data, f, indent=4)
                                    
                                    if discount_applied:
                                        print(f"\nThank you! You have purchased {game_title}.")
                                        print(f"Original price: €{game_info['price']:.2f}")
                                        print(f"Discount ({discount_applied['percentage']}%): -€{game_info['price'] * (discount_applied['percentage'] / 100):.2f}")
                                        print(f"Final price: €{final_price:.2f}")
                                    else:
                                        print(f"\nThank you! You have purchased {game_title} for €{game_info['price']}.")
                                    wait = questionary.text("Press Enter to return to the Customer panel.").ask()
                                else:
                                    print("\nSorry, this game is out of stock.")
                                    wait = questionary.text("Press Enter to return to the Customer panel.").ask()
                            
                            elif buy_menu == "Add to Basket":
                                customer_basket.append({
                                    'title': game_title,
                                    'price': game_info['price']
                                })
                                print(f"\n{game_title} has been added to your basket!")
                                wait = questionary.text("Press Enter to return to the Customer panel.").ask()

        elif customer_panel == "Search for Game":
            games_dir = "games"
            if not os.path.exists(games_dir) or not os.listdir(games_dir):
                print("No games available at the moment.")
            else:
                # Get list of available games
                game_titles = os.listdir(games_dir)
                available_games = []
                
                for game_title in game_titles:
                    game_path = os.path.join(games_dir, game_title, "game_info.json")
                    if os.path.exists(game_path):
                        with open(game_path, "r") as f:
                            game_data = json.load(f)
                            stock = game_data.get('stock', 0)
                            if stock > 0:
                                available_games.append(game_title)
                
                if not available_games:
                    print("No games in stock at the moment.")
                else:
                    # Search for a game using autocomplete
                    selected_game = questionary.autocomplete(
                        "Search for a game:",
                        choices=available_games
                    ).ask()
                    
                    if selected_game is not None:
                        # Display game details
                        game_path = os.path.join(games_dir, selected_game, "game_info.json")
                        if os.path.exists(game_path):
                            with open(game_path, "r") as f:
                                game_data = json.load(f)
                                price = game_data.get('price', 'N/A')
                                stock = game_data.get('stock', 0)
                                synopsis = game_data.get('synopsis', 'N/A')
                                print(f"\n--- {selected_game} ---")
                                print(f"Price: €{price}")
                                print(f"Status: {'available' if stock > 0 else 'out of stock'}")
                                print(f"Synopsis:")
                                print(f"  {synopsis}")
                                print()
                                
                                # Show Buy/Add to Basket/Back menu
                                buy_menu = questionary.select(
                                    "What would you like to do?",
                                    choices=["Buy", "Add to Basket", "Back"]
                                ).ask()
                                
                                if buy_menu == "Buy":
                                    if stock > 0:
                                        # Check for applicable discount (find the biggest one)
                                        discounts = load_discounts()
                                        final_price = price
                                        discount_applied = None
                                        
                                        # Find all applicable discounts and select the biggest one
                                        applicable_discounts = [disc for disc in discounts if selected_game in disc.get('games', [])]
                                        if applicable_discounts:
                                            discount_applied = max(applicable_discounts, key=lambda x: x['percentage'])
                                            discount_amount = final_price * (discount_applied['percentage'] / 100)
                                            final_price = final_price - discount_amount
                                        
                                        # Reduce stock by 1
                                        game_data['stock'] = stock - 1
                                        with open(game_path, "w") as f:
                                            json.dump(game_data, f, indent=4)
                                        
                                        if discount_applied:
                                            print(f"\nThank you! You have purchased {selected_game}.")
                                            print(f"Original price: €{price:.2f}")
                                            print(f"Discount ({discount_applied['percentage']}%): -€{price * (discount_applied['percentage'] / 100):.2f}")
                                            print(f"Final price: €{final_price:.2f}")
                                        else:
                                            print(f"\nThank you! You have purchased {selected_game} for €{price}.")
                                        wait = questionary.text("Press Enter to return to the Customer panel.").ask()
                                    else:
                                        print("\nSorry, this game is out of stock.")
                                        wait = questionary.text("Press Enter to return to the Customer panel.").ask()
                                
                                elif buy_menu == "Add to Basket":
                                    customer_basket.append({
                                        'title': selected_game,
                                        'price': price
                                    })
                                    print(f"\n{selected_game} has been added to your basket!")
                                    wait = questionary.text("Press Enter to return to the Customer panel.").ask()

        elif customer_panel == "View Basket":
            if not customer_basket:
                print("\nYour basket is empty.")
                wait = questionary.text("Press Enter to return to the Customer panel.").ask()
            else:
                # Show basket with options
                basket_action = None
                while basket_action != "Back":
                    print("\n--- Your Basket ---")
                    total_price = 0
                    for i, item in enumerate(customer_basket, 1):
                        print(f"{i}. {item['title']} - €{item['price']}")
                        # Handle price as string or number
                        try:
                            price = float(item['price'])
                            total_price += price
                        except (ValueError, TypeError):
                            pass
                    print(f"\nTotal: €{total_price:.2f}")
                    print()
                    
                    basket_action = questionary.select(
                        "What would you like to do?",
                        choices=["Remove Item", "Buy", "Back"]
                    ).ask()
                    
                    if basket_action == "Remove Item":
                        # Create list of items to remove from
                        item_choices = [f"{i}. {item['title']} - €{item['price']}" for i, item in enumerate(customer_basket, 1)]
                        item_choices.append("Cancel")
                        
                        item_to_remove = questionary.select(
                            "Select an item to remove:",
                            choices=item_choices
                        ).ask()
                        
                        if item_to_remove and item_to_remove != "Cancel":
                            # Extract item index from the choice
                            item_index = int(item_to_remove.split(".")[0]) - 1
                            if 0 <= item_index < len(customer_basket):
                                removed_item = customer_basket.pop(item_index)
                                print(f"\n{removed_item['title']} has been removed from your basket.")
                                wait = questionary.text("Press Enter to continue.").ask()
                    
                    elif basket_action == "Buy":
                        # Process purchase with discounts
                        games_dir = "games"
                        all_purchases_success = True
                        discounts = load_discounts()
                        final_total = 0
                        purchase_details = []
                        
                        for item in customer_basket:
                            game_title = item['title']
                            game_price = item['price']
                            game_path = os.path.join(games_dir, game_title, "game_info.json")
                            
                            if os.path.exists(game_path):
                                with open(game_path, "r") as f:
                                    game_data = json.load(f)
                                
                                if game_data.get('stock', 0) > 0:
                                    # Check for applicable discount (find the biggest one)
                                    final_price = game_price
                                    discount_applied = None
                                    
                                    # Find all applicable discounts and select the biggest one
                                    applicable_discounts = [disc for disc in discounts if game_title in disc.get('games', [])]
                                    if applicable_discounts:
                                        discount_applied = max(applicable_discounts, key=lambda x: x['percentage'])
                                        discount_amount = final_price * (discount_applied['percentage'] / 100)
                                        final_price = final_price - discount_amount
                                    
                                    # Reduce stock by 1
                                    game_data['stock'] = game_data.get('stock', 0) - 1
                                    with open(game_path, "w") as f:
                                        json.dump(game_data, f, indent=4)
                                    
                                    final_total += final_price
                                    purchase_details.append({
                                        'title': game_title,
                                        'original_price': game_price,
                                        'final_price': final_price,
                                        'discount': discount_applied
                                    })
                                else:
                                    all_purchases_success = False
                                    print(f"\nSorry, {game_title} is out of stock.")
                        
                        if all_purchases_success and customer_basket:
                            print(f"\nThank you! You have purchased {len(customer_basket)} game(s).")
                            for detail in purchase_details:
                                if detail['discount']:
                                    print(f"\n{detail['title']}:")
                                    print(f"  Original: €{detail['original_price']:.2f}")
                                    print(f"  Discount ({detail['discount']['percentage']}%): -€{detail['original_price'] * (detail['discount']['percentage'] / 100):.2f}")
                                    print(f"  Final: €{detail['final_price']:.2f}")
                                else:
                                    print(f"\n{detail['title']}: €{detail['final_price']:.2f}")
                            print(f"\nTotal: €{final_total:.2f}")
                            customer_basket = []
                            wait = questionary.text("Press Enter to return to the Customer panel.").ask()
                            basket_action = "Back"
                        else:
                            if customer_basket:
                                print("\nSome items could not be purchased due to stock issues.")
                                wait = questionary.text("Press Enter to continue.").ask()

        elif customer_panel == "View Discounts":
            discounts = load_discounts()
            if not discounts:
                print("\nNo discounts available at the moment.")
            else:
                print("\n--- Active Discounts ---")
                for disc in discounts:
                    games_list = ", ".join(disc.get('games', []))
                    print(f"\nCode: {disc['code']}")
                    print(f"Name: {disc['name']}")
                    print(f"Discount: {disc['percentage']}%")
                    print(f"Applies to: {games_list}")
            wait = questionary.text("\nPress Enter to return to the Customer panel.").ask()

        elif customer_panel == "Exit":
            print("Thank you for shopping at Respawn Point! Goodbye!")
            exit_app = True
            break

    if exit_app:
        break