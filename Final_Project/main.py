from customers import login
from orders import new_order, verify, change_order, save_order, order_receipt

def main():
        customer = login()
        order = new_order(customer)
while not verify(order):
    order = change_order(order)
    save_order(order)
    order_receipt(order)

choice_delete = input("Do you want to delete an old, past order? (Y/N)").strip().lower()
if choice_delete == "y":
    customer_name = input("Enter your name to remove past order(s): ").strip()
    delete_order(customer_name)

if __name__ == "__main__":
    main()