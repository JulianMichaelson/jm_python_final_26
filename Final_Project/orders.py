from datetime import datetime

ORDERS_FILE = "orders.txt"

PIZZA_SIZES = ("Small", "Medium", "Large", "Extra Large")
PIZZA_CHOICES = ("Pepperoni", "Cheese", "Sausage", "Meat Lovers", "Veggie")
PIZZA_TYPE = ("Thin Crust", "Thick Crust", "Chicago Style", "New York Style", "Detroit Style", "Stuffed Crust")
DRINKS = ("Water", "Coke", "Dr. Pepper", "Lemonade", "Sweet Tea", "Beer")
SIDES = ("5 Count Hot Wings", "Jalapeno Chips", "Mozzarella Sticks")

def past_orders(customer):
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as file:
            lines = file.read().strip().splitlines()

        if not lines:
            print("No past orders found.")
            return None

        print("\nRecent orders:")
        for line in lines[-10:]:
            print(line)

        return 1

    except FileNotFoundError:
        print("No past orders found.")
    return None

def new_order(customer):
    print("\n--------PIZZA MENU--------")
    print("Sizes:", PIZZA_SIZES)
    print("Pizzas:", PIZZA_CHOICES)
    print("Crusts:", PIZZA_TYPE)
    print("Drinks:", DRINKS)
    print("Sides:", SIDES)

    order = {"customer_name": customer["customer_name"], "phone_number": customer["phone_number"], "size": input("Choose a size: ").title().strip(), "pizza": input("Choose a pizza: ").title().strip(), "crust": input("Choose a crust: ").title().strip(), "drink": input("Choose a drink: ").title().strip(), "side": input("Choose a side: ").title().strip()
        }
    return order

def verify(order):
    print("\nPlease verify that your order is correct to your choosing:")
    print(f"Size: {order['size']}")
    print(f"Pizza: {order['pizza']}")
    print(f"Crust: {order['crust']}")
    print(f"Drink: {order['drink']}")
    print(f"Side: {order['side']}")

    answer = input("Is your order correct? (Y/N): ").strip().lower()
    return answer == "y"
# verifies if your order is correct to your liking, if not you are able to edit something of your choosing

def save_order(order):
    record = {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Customer": order["customer_name"], "Phone number": order["phone_number"], "Size": order["size"], "Pizza": order["pizza"], "Crust": order["crust"], "Drink": order["drink"], "Side": order["side"],}

    with open(ORDERS_FILE, "a", encoding="utf-8") as file:
        for label, value in record.items():
            file.write(f"{label}: {value}\n")
        file.write("\n")

def delete_order(customer_name):
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()

        remaining = []
        for line in lines:
            if customer_name not in line:
                remaining.append(line)

        with open(ORDERS_FILE, "w", encoding="utf-8") as file:
            file.write("\n".join(remaining))

        print(f"Deleted an past orders for, {customer_name}.")

    except FileNotFoundError:
        print("No past orders found to delete")
    except OSError as e:
        print(f"Could not delete order: {e}")

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
        order["size"] = input("Choose a pizza size: ").title().strip()
    elif choice == "2":
        print(PIZZA_CHOICES)
        order["pizza"] = input("Choose a pizza type: ").title().strip()
    elif choice == "3":
        print(PIZZA_TYPE)
        order["crust"] = input("Choose a crust: ").title().strip()
    elif choice == "4":
        print(DRINKS)
        order["drink"] = input("Choose a drink: ").title().strip()
    elif choice == "5":
        print(SIDES)
        order["side"] = input("Choose a side: ").title().strip()
    else:
        print("That choice wasn't recognized.")

    return order
    # display numbered parts of order allow them to change

from customers import login

def order_receipt(order):
    print("\n---------YOUR PIZZA ORDER RECEIPT---------")
    print(f"Customer Name: {order['customer_name']}")
    print(f"Phone Number: {order['phone_number']}")
    print(f"Pizza Size: {order['size']}")
    print(f"Pizza Type: {order['pizza']}")
    print(f"Crust: {order['crust']}")
    print(f"Drink: {order['drink']}")
    print(f"Side: {order['side']}")
    print("---------------------------")
    print("Thank you for ordering from us, enjoy the food and come back again!")
    # Display final order