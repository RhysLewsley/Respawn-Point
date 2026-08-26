import json
import os
import questionary

json_file = "employee_list.json"


def load_employees():
    """Safely load the employee list from the JSON file."""
    if not os.path.exists(json_file):
        return []
    try:
        with open(json_file, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []  # Return empty list if file is corrupted


def save_employees(employees):
    """Save the employee list back to the JSON file."""
    with open(json_file, "w") as f:
        json.dump(employees, f, indent=4)


# Outer loop to keep the main application running
while True:
    exit_app = False
    answer = questionary.select(
        "Welcome to the Respawn Point app! Please select an option below:",
        choices=["Admin", "Employee", "Customer", "Exit App"],
    ).ask()

    if answer == "Exit App" or answer is None:
        print("Goodbye!")
        break

    # Admin Panel Sub-menu Loop
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
            print("You selected Remove Employee")

        elif admin_answer == "Edit Employee":
            print("You selected Edit Employee")

        elif admin_answer == "View Employees":
            employees = load_employees()
            if not employees:
                print("No employees found.")
            else:
                print("\nCurrent Employees:")
                for emp in employees:
                    print(f"- {emp}")
                print()  # Add an extra newline for spacing

        elif admin_answer == "Exit" or admin_answer is None:
            print("Goodbye!")
            exit_app = True
            break

    if exit_app:
        break
