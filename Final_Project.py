"""
Final Project - Step 1
Copy as a new step with new comment each week
This week: Define constants, create stubs, create menu

"""
# Globals - Variables declared outside of all of the functions are global

# Constants - (still globals) Don't change while project is running

from datetime import datetime

ORDERS_FILE = "orders.txt"

PIZZA_SIZES = ("Small", "Medium", "Large", "Extra Large")
PIZZA_CHOICES = ("Pepperoni", "Cheese", "Sausage", "Meat Lovers", "Veggie")
PIZZA_TYPE = ("Thin Crust", "Thick Crust", "Chicago Style", "New York Style", "Detroit Style", "Stuffed Crust")
DRINKS = ("Water", "Coke", "Dr. Pepper", "Lemonade", "Sweet Tea", "Beer")
SIDES = ("5 Count Buffalo Wings", "5 Count BBQ Wings", "5 Count Hot Wings", "5 Count Garlic Parmesan Wings", "5 Count Lemon Pepper Wings", "Salt and Vinegar Chips", "Sour Cream and Onion Chips", "5 Count Mozzarella Sticks with Marinara")
MENU = "menu.txt"

def login():
    # gets login info
    # returns login ID
    # Gets the users information like their name
        # will see if the user is already existing
    print("Please login to your account")
    employee_id = input("Please enter your login ID: ").strip()
    return employee_id
    # Have them text with ID and names, check if on it. If on it display name, number, extension to get them

def past_orders(employee):
    # check for and display most recent 5 orders if there are any, ask if they want to reorder give them the menu
    # return number of past order or 6 if they went to create a new order
    return None

def new_order(employee):
    print(f"Pizza Sizes: {PIZZA_SIZES}")
    size = input("Choose a size: ").title().strip()

    print(f"Pizza choices: {PIZZA_CHOICES}")
    pizza = input("Choose a pizza: ").title().strip()

    print(f"Crust types: {PIZZA_TYPE}")
    pizza_type = input("Choose a crust: ").title().strip()

    print(f"Drinks: {DRINKS}")
    drink = input("Choose a drink: ").title().strip()

    print(f"Sides: {SIDES}")
    side = input("Choose a side: ").title().strip()

    order = [employee, size, pizza, pizza_type, drink, side]
    return order

def verify(order):
    print("\nPlease verify that your order is correct to your choosing:")
    print(f"Size: {order[1]}")
    print(f"Pizza: {order[2]}")
    print(f"Crust: {order[3]}")
    print(f"Drink: {order[4]}")
    print(f"Side: {order[5]}")

    answer = input("Is your order correct? (Y/N): ").strip().lower()
    return answer == "y"

def save_order(order):
    record = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Employee ID": order[0],
        "Size": order[1],
        "Pizza": order[2],
        "Crust": order[3],
        "Drink": order[4],
        "Side": order[5],
    }

    with open(ORDERS_FILE, "a", encoding="utf-8") as file:
        for label, value in record.items():
            file.write(f"{label}: {value}\n")
        file.write("\n")

def change_order(order):
    print("\nWhat would you like to change from your order?")
    print("1. Pizza Size")
    print("2. Pizza Type")
    print("3. Crust")
    print("4. Drink")
    print("5. Side")

    choice = input("Choose 1-5: ").strip()

    if choice == "1":
        print(PIZZA_SIZES)
        order[1] = input("Choose a pizza size: ").title().strip()
    elif choice == "2":
        print(PIZZA_CHOICES)
        order[2] = input("Choose a pizza type: ").title().strip()
    elif choice == "3":
        print(PIZZA_TYPE)
        order[3] = input("Choose a crust: ").title().strip()
    elif choice == "4":
        print(DRINKS)
        order[4] = input("Choose a drink: ").title().strip()
    elif choice == "5":
        print(SIDES)
        order[5] = input("Choose a side: ").title().strip()
    else:
        print("That choice wasn't recognized.")

    return order
    # display numbered parts of order allow them to change

def order_receipt(order):
    print("---------YOUR PIZZA ORDER RECEIPT---------")
    print(f"Employee ID: {order[0]}")
    print(f"Pizza Size: {order[1]}")
    print(f"Pizza Type: {order[2]}")
    print(f"Crust: {order[3]}")
    print(f"Drink: {order[4]}")
    print(f"Side: {order[5]}")
    print("---------------------------")
    print("Thank you for ordering from us, enjoy the food and come back again!")
    # Display final order

def main():
    employee_id = login()
    order = past_orders(employee_id)
    if order is None:
        order = new_order(employee_id)
    while not verify(order):
        order = change_order(order)
    save_order(order)
    order_receipt(order)
main()