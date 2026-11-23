from customers import login
from orders import new_order, verify, change_order, save_order, delete_order


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
    print("Thank you for ordering from us, Enjoy the food and come back again!")


def main():
    customer = login()
    if customer is None:
        return

    order = new_order(customer)
    while not verify(order):
        order = change_order(order)

    save_order(order)
    order_receipt(order)

    choice_delete = input(
        "Do you want to delete an old order? (Y/N): "
    ).strip().lower()
    if choice_delete == "y":
        customer_name = input(
            "Enter your name to remove past orders: "
        ).strip()
        delete_order(customer_name)

if __name__ == "__main__":
    main()