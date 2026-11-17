from customers import login
from orders import new_order, verify, change_order, save_order, order_receipt

def main():
    customer = login()
    order = new_order(customer)
    while not verify(order):
        order = change_order(order)
    save_order(order)
    order_receipt(order)

if __name__ == "__main__":
    main()