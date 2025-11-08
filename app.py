import logging
from decimal import Decimal
from db import engine, Base
from crud import (
    create_user, list_users,
    create_category, list_categories,
    create_expense, list_expenses,
    update_expense, delete_expense
)
from models import User, Category, Expense

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def init_db():
    Base.metadata.create_all(engine)

# ---------- Input Helpers ----------
def input_nonempty(prompt, max_len=255):
    while True:
        s = input(prompt).strip()
        if not s:
            print("Please enter something.")
            continue
        if len(s) > max_len:
            print(f"Too long (max {max_len} chars).")
            continue
        return s

def input_decimal(prompt):
    while True:
        s = input(prompt).strip()
        try:
            d = Decimal(s)
            if d < 0:
                print("Amount must be non-negative.")
                continue
            return d.quantize(Decimal("0.01"))
        except Exception:
            print("Enter a valid number (like 100.50).")

def choose_from_list(items, title):
    if not items:
        raise ValueError("No items to choose from.")
    print(f"\nChoose {title}:")
    for i, it in enumerate(items, 1):
        if isinstance(it, User):
            print(f" {i}) {it.username}")
        elif isinstance(it, Category):
            print(f" {i}) {it.name}")
        elif isinstance(it, Expense):
            print(f" {i}) {it.id} | {it.name} | ₹{float(it.amount):.2f}")
    while True:
        n = input(f"Enter number (1-{len(items)}): ").strip()
        if n.isdigit() and 1 <= int(n) <= len(items):
            return int(n) - 1
        print("Invalid choice.")

# ---------- CLI Commands ----------
def cmd_create_user():
    name = input_nonempty("Username: ", 100)
    email = input("Email (optional): ").strip() or None
    try:
        u = create_user(name, email)
        print("✅ Created user:", u.username)
    except Exception as e:
        print("Error:", e)

def cmd_create_category():
    name = input_nonempty("Category name: ", 100)
    try:
        c = create_category(name)
        print("✅ Created category:", c.name)
    except Exception as e:
        print("Error:", e)

def cmd_add_expense():
    users = list_users()
    if not users:
        print("No users. Create one first.")
        return
    user = users[choose_from_list(users, "user")]

    cats = list_categories()
    if not cats:
        print("No categories. Create one first.")
        return
    cat = cats[choose_from_list(cats, "category")]

    name = input_nonempty("Expense name: ")
    amount = input_decimal("Amount (₹): ")
    e = create_expense(user.id, cat.id, name, amount)
    print(f"✅ Expense saved (id={e.id})")

def cmd_list_expenses():
    exps = list_expenses()
    if not exps:
        print("No expenses found.")
        return
    print("\nYour Expenses:")
    for e in exps:
        print(f"ID:{e.id} | User:{e.user.username} | Category:{e.category.name} | {e.name} | ₹{float(e.amount):.2f} | Created:{e.created_at} | Updated:{e.updated_at}")

def cmd_update_expense():
    exps = list_expenses()
    if not exps:
        print("No expenses to update.")
        return
    exp = exps[choose_from_list(exps, "expense")]
    new_name = input(f"New name [{exp.name}]: ").strip() or exp.name
    new_amount = input(f"New amount [{float(exp.amount):.2f}]: ").strip()
    if new_amount:
        try:
            new_amount = Decimal(new_amount)
        except Exception:
            print("Invalid amount.")
            return
    else:
        new_amount = exp.amount
    cats = list_categories()
    for i, c in enumerate(cats, 1):
        print(f" {i}) {c.name}")
    cat_choice = input("Choose new category or Enter to keep current: ").strip()
    if cat_choice:
        cat_id = cats[int(cat_choice) - 1].id
    else:
        cat_id = exp.category_id

    updated = update_expense(exp.id, name=new_name, amount=new_amount, category_id=cat_id)
    print("✅ Updated successfully. (updated_at auto-changed)")

def cmd_delete_expense():
    exps = list_expenses()
    if not exps:
        print("No expenses to delete.")
        return
    exp = exps[choose_from_list(exps, "expense")]
    confirm = input(f"Type 'yes' or 'y' to delete {exp.name}: ").strip().lower()
    if confirm == "yes" or "y":
        delete_expense(exp.id)
        print("✅ Deleted.")
    else:
        print("Cancelled.")

# ---------- Menu ----------
def show_menu():
    print("\n===== Expense Tracker =====")
    print("1) Create user")
    print("2) Create category")
    print("3) Add expense")
    print("4) List expenses")
    print("5) Update expense")
    print("6) Delete expense")
    print("0) Exit")

def main():
    init_db()
    while True:
        show_menu()
        c = input("Choose option: ").strip()
        if c == "1": cmd_create_user()
        elif c == "2": cmd_create_category()
        elif c == "3": cmd_add_expense()
        elif c == "4": cmd_list_expenses()
        elif c == "5": cmd_update_expense()
        elif c == "6": cmd_delete_expense()
        elif c == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
