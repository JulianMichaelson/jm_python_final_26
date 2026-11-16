"""Julians Pizza point-of-sale app."""

import csv
import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import streamlit as st

from read_menu import read_menu


APP_DIR = Path(__file__).resolve().parent
MENU_FILE = APP_DIR / "menu_config.txt"
EMPLOYEES_FILE = APP_DIR / "employees.txt"
ORDERS_FILE = APP_DIR / "orders.txt"

PIZZA_SIZE_PRICES = {
    "Small": 899,
    "Medium": 1199,
    "Large": 1499,
    "Extra Large": 1799,
}
PIZZA_CHOICE_EXTRAS = {
    "Cheese": 0,
    "Pepperoni": 100,
    "Sausage": 100,
    "Meat Lovers": 250,
    "Veggie": 150,
}
CRUST_EXTRAS = {
    "Thin Crust": 0,
    "Thick Crust": 100,
    "Chicago Style": 250,
    "New York Style": 100,
    "Detroit Style": 200,
    "Stuffed Crust": 250,
}
DRINK_PRICES = {
    "Water": 100,
    "Coke": 200,
    "Dr. Pepper": 200,
    "Lemonade": 225,
    "Sweet Tea": 200,
    "Beer": 400,
}
SIDE_PRICES = {
    "5 Count Buffalo Wings": 699,
    "5 Count BBQ Wings": 699,
    "5 Count Hot Wings": 699,
    "5 Count Garlic Parmesan Wings": 699,
    "5 Count Lemon Pepper Wings": 699,
    "Salt and Vinegar Chips": 199,
    "Sour Cream and Onion Chips": 199,
    "5 Count Mozzarella Sticks with Marinara": 549,
}


def money(cents: int) -> str:
    return f"${cents // 100:,}.{cents % 100:02d}"


def load_employees() -> dict[str, str]:
    if not EMPLOYEES_FILE.exists() or EMPLOYEES_FILE.stat().st_size == 0:
        return {}

    with EMPLOYEES_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != ["employee_id", "name"]:
            raise ValueError(
                "employees.txt must have the header: employee_id,name"
            )
        return {
            row["employee_id"].strip(): row["name"].strip()
            for row in reader
            if row.get("employee_id", "").strip() and row.get("name", "").strip()
        }


def register_employee(employee_id: str, name: str) -> None:
    write_header = not EMPLOYEES_FILE.exists() or EMPLOYEES_FILE.stat().st_size == 0
    with EMPLOYEES_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(["employee_id", "name"])
        writer.writerow([employee_id, name])


def validate_menu(menu: dict[str, list[str]]) -> None:
    required = ("PIZZA SIZE", "PIZZA CHOICE", "PIZZA TYPE", "SIDE", "DRINK")
    missing_categories = [category for category in required if not menu.get(category)]
    if missing_categories:
        raise ValueError(
            "menu_config.txt is missing menu categories: "
            + ", ".join(missing_categories)
        )

    price_categories = {
        "PIZZA SIZE": PIZZA_SIZE_PRICES,
        "PIZZA CHOICE": PIZZA_CHOICE_EXTRAS,
        "PIZZA TYPE": CRUST_EXTRAS,
        "SIDE": SIDE_PRICES,
        "DRINK": DRINK_PRICES,
    }
    for category, price_list in price_categories.items():
        missing_items = [item for item in menu[category] if item not in price_list]
        if missing_items:
            raise ValueError(
                f"Add prices in Final_Project.py for {category}: "
                + ", ".join(missing_items)
            )


def load_recent_orders() -> list[dict]:
    if not ORDERS_FILE.exists():
        return []

    orders = []
    with ORDERS_FILE.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                orders.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Could not read orders.txt line {line_number}: {error.msg}"
                ) from error
    return list(reversed(orders[-5:]))


def save_order(order: dict) -> None:
    with ORDERS_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(order, ensure_ascii=False) + "\n")


def add_to_cart(description: str, quantity: int, unit_price_cents: int) -> None:
    st.session_state.cart.append(
        {
            "description": description,
            "quantity": quantity,
            "unit_price_cents": unit_price_cents,
        }
    )


def render_sign_in() -> None:
    employees = load_employees()
    st.sidebar.subheader("Team sign-in")

    if st.session_state.get("employee_id"):
        st.sidebar.success(
            f"Signed in: {st.session_state.employee_name} "
            f"({st.session_state.employee_id})"
        )
        if st.sidebar.button("Sign out", use_container_width=True):
            del st.session_state["employee_id"]
            del st.session_state["employee_name"]
            st.rerun()
        return

    mode = st.sidebar.radio("Choose an option", ("Sign in", "Register employee"))
    if mode == "Sign in":
        if not employees:
            st.sidebar.info("No team members yet. Register an employee to get started.")
        with st.sidebar.form("sign_in_form"):
            employee_id = st.text_input("Employee ID").strip()
            submitted = st.form_submit_button("Sign in", use_container_width=True)
        if submitted:
            if employee_id in employees:
                st.session_state.employee_id = employee_id
                st.session_state.employee_name = employees[employee_id]
                st.rerun()
            st.sidebar.error("That employee ID was not found. Register first.")
    else:
        with st.sidebar.form("register_form"):
            employee_id = st.text_input("Choose an employee ID").strip()
            name = st.text_input("Full name").strip()
            submitted = st.form_submit_button(
                "Register and sign in", use_container_width=True
            )
        if submitted:
            if not employee_id or not name:
                st.sidebar.error("Enter both an employee ID and full name.")
            elif employee_id in employees:
                st.sidebar.error("That employee ID is already registered.")
            else:
                register_employee(employee_id, name)
                st.session_state.employee_id = employee_id
                st.session_state.employee_name = name
                st.rerun()


def render_menu(menu: dict[str, list[str]]) -> None:
    st.subheader("Build an order")
    st.caption("Choose an item, set the quantity, and add it to the order.")

    with st.form("add_item_form"):
        category = st.selectbox("Menu category", ("Pizza", "Drinks", "Sides"))

        if category == "Pizza":
            size = st.selectbox("Size", menu["PIZZA SIZE"])
            pizza = st.selectbox("Pizza", menu["PIZZA CHOICE"])
            crust = st.selectbox("Crust", menu["PIZZA TYPE"])
            quantity = st.selectbox("Quantity", range(1, 11), index=0)
            unit_price = (
                PIZZA_SIZE_PRICES[size]
                + PIZZA_CHOICE_EXTRAS[pizza]
                + CRUST_EXTRAS[crust]
            )
            description = f"{size} {pizza} Pizza ({crust})"
        elif category == "Drinks":
            item = st.selectbox("Drink", menu["DRINK"])
            quantity = st.selectbox("Quantity", range(1, 11), index=0)
            unit_price = DRINK_PRICES[item]
            description = item
        else:
            item = st.selectbox("Side", menu["SIDE"])
            quantity = st.selectbox("Quantity", range(1, 11), index=0)
            unit_price = SIDE_PRICES[item]
            description = item

        st.write(f"Unit price: **{money(unit_price)}**")
        submitted = st.form_submit_button(
            "Add to order", type="primary", use_container_width=True
        )

    if submitted:
        add_to_cart(description, quantity, unit_price)
        st.success(f"Added {quantity} × {description}.")


def render_cart() -> None:
    st.subheader("Your order")
    cart = st.session_state.cart
    if not cart:
        st.info("Your order is empty. Add items from the Menu tab.")
    else:
        total = 0
        for index, item in enumerate(cart):
            item_total = item["quantity"] * item["unit_price_cents"]
            total += item_total
            item_col, price_col, remove_col = st.columns((6, 2, 1))
            item_col.write(
                f"**{item['quantity']} × {item['description']}**"
            )
            price_col.write(money(item_total))
            if remove_col.button("✕", key=f"remove_{index}", help="Remove item"):
                cart.pop(index)
                st.rerun()

        st.divider()
        st.markdown(f"### Total: {money(total)}")
        st.caption("Sales tax is not included.")

        with st.form("checkout_form"):
            customer_name = st.text_input("Order name (optional)").strip()
            submitted = st.form_submit_button(
                "Place order", type="primary", use_container_width=True
            )

        if submitted:
            order = {
                "order_id": uuid4().hex[:8].upper(),
                "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
                "employee_id": st.session_state.employee_id,
                "employee_name": st.session_state.employee_name,
                "customer_name": customer_name,
                "items": cart.copy(),
                "total_cents": total,
            }
            save_order(order)
            st.session_state.cart = []
            st.success(f"Order {order['order_id']} placed. Thank you!")
            st.download_button(
                "Download receipt",
                data=receipt_text(order),
                file_name=f"receipt-{order['order_id']}.txt",
                mime="text/plain",
            )


def receipt_text(order: dict) -> str:
    lines = [
        "Julians Pizza",
        f"Order: {order['order_id']}",
        f"Time: {order['timestamp']}",
        f"Employee: {order['employee_name']} ({order['employee_id']})",
    ]
    if order["customer_name"]:
        lines.append(f"Order name: {order['customer_name']}")
    lines.extend(["", "Items:"])
    for item in order["items"]:
        line_total = item["quantity"] * item["unit_price_cents"]
        lines.append(
            f"{item['quantity']} x {item['description']} - {money(line_total)}"
        )
    lines.extend(
        [
            "",
            f"Total: {money(order['total_cents'])}",
            "Sales tax is not included.",
            "Thank you for choosing Julians Pizza!",
        ]
    )
    return "\n".join(lines)


def render_recent_orders() -> None:
    st.subheader("Recent orders")
    orders = load_recent_orders()
    if not orders:
        st.caption("Completed orders will appear here.")
        return

    for order in orders:
        customer = order.get("customer_name") or "Walk-in"
        with st.expander(
            f"{order['order_id']} · {customer} · {money(order['total_cents'])}"
        ):
            st.caption(
                f"{order['timestamp']} · "
                f"{order['employee_name']} ({order['employee_id']})"
            )
            for item in order["items"]:
                st.write(
                    f"{item['quantity']} × {item['description']} — "
                    f"{money(item['quantity'] * item['unit_price_cents'])}"
                )


def main() -> None:
    st.set_page_config(page_title="Julians Pizza", page_icon="🍕", layout="wide")
    st.markdown(
        """
        <style>
        .stApp { background: #fffaf0; }
        h1, h2, h3 { color: #a3261c; }
        div.stButton > button[kind="primary"],
        div.stFormSubmitButton > button[kind="primary"] {
            background: #e85d04;
            border-color: #e85d04;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("🍕 Julians Pizza")
    st.caption("Fresh pizza, easy ordering.")

    st.session_state.setdefault("cart", [])
    try:
        render_sign_in()
    except (OSError, ValueError) as error:
        st.sidebar.error(str(error))
        return

    if not st.session_state.get("employee_id"):
        st.info("Sign in from the sidebar to start an order.")
        return

    if not MENU_FILE.exists():
        st.error(f"Required menu file not found: {MENU_FILE.name}")
        return

    try:
        menu = read_menu(MENU_FILE)
        validate_menu(menu)
    except (OSError, ValueError) as error:
        st.error(str(error))
        return

    menu_tab, order_tab = st.tabs(("Menu", "Order"))
    with menu_tab:
        render_menu(menu)
    with order_tab:
        render_cart()
        st.divider()
        try:
            render_recent_orders()
        except (OSError, ValueError) as error:
            st.error(str(error))


if __name__ == "__main__":
    main()
