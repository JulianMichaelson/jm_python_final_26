CUSTOMER_FILE = "customers.txt"

def login():
    customer_name = input("Please enter your name: ").strip()
    phone_number = input("Please enter your phone number: ").strip()

    with open(CUSTOMER_FILE, "a", encoding="utf-8") as f:
        f.write(f"{customer_name},{phone_number}\n")

    return {"customer_name": customer_name, "phone_number": phone_number}