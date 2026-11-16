"""
-----------------------------------------------------------------------
ASSIGNMENT 12A: THE CONFIGURABLE MENU & AUDITOR
-----------------------------------------------------------------------
[ ] 1. Header Docstring included.
[ ] 2. PHASE 1: External menu_config.txt file created in workspace.
[ ] 3. Program reads and parses the .txt file into a Dictionary.
[ ] 4. PHASE 2: break the dictionary into individual variables.
[ ] 6. Print each category and its details
[ ] 7. try/except used to prevent crashes on FileNotFoundError.
-----------------------------------------------------------------------
"""
from pathlib import Path


# This reads the external file and creates a dictionary of all the items within the menu

def read_menu(file_path=None):
    menu = {}
    source = Path(file_path) if file_path else Path(__file__).with_name("menu_config.txt")

    try:
        with source.open("r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue
                parts = [part.strip() for part in line.split(",")]
                if len(parts) < 2 or not parts[0] or any(not item for item in parts[1:]):
                    raise ValueError(f"Invalid menu entry: {line.rstrip()}")

                category = parts[0]
                details = parts[1:]

                if category in menu:
                    raise ValueError(f"Duplicate menu category: {category}")
                menu[category] = details

        return menu

    except FileNotFoundError:
        print(f"Error: {source.name} not found.")
        return menu

# This breaks the dictionary into individual variables, making it more coherent and structured

def split_into_variables(menu):

    pizza_sizes = menu.get("PIZZA SIZE", [])
    pizza_choices = menu.get("PIZZA CHOICE", [])
    pizza_types = menu.get("PIZZA TYPE", [])
    sides = menu.get("SIDE", [])
    drinks = menu.get("DRINK", [])

    return pizza_sizes, pizza_choices, pizza_types, sides, drinks

# This part prints each menu category and its following details

def print_menu(pizza_sizes, pizza_choices, pizza_types, sides, drinks):

    print("\n" + "=" * 45)
    print("           PIZZA MENU")
    print("=" * 45)

    print("\nPIZZA SIZES")
    for item in pizza_sizes:
        print(f"  - {item}")

    print("\nPIZZA CHOICES")
    for item in pizza_choices:
        print(f"  - {item}")

    print("\nPIZZA TYPES")
    for item in pizza_types:
        print(f"  - {item}")

    print("\nSIDES")
    for item in sides:
        print(f"  - {item}")

    print("\nDRINKS")
    for item in drinks:
        print(f"  - {item}")

    print("\n"+ "=" * 45)

# the first point of all this code tells what to run and in the following order!

def main():

    menu_items = read_menu()

    pizza_sizes, pizza_choices, pizza_types, sides, drinks = split_into_variables(menu_items)

    print_menu(pizza_sizes, pizza_choices, pizza_types, sides, drinks)

if __name__ == "__main__":
    main()