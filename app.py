import logging
from decimal import Decimal
from db import engine, Base
from crud import (
    create_user, list_users,
    create_category, list_categories,
    create_expense, list_expenses,
    update_expense, delete_expense,
    authenticate_user, get_expense_aggregates_by_date
)
from models import User, Category, Expense
import getpass
from datetime import datetime
import os

# plotting
import matplotlib.pyplot as plt

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

# ---------- AUTH (CLI) ----------
current_user = None  # will hold User object when logged in

def cmd_register():
    print("\n--- Register new user ---")
    username = input_nonempty("Username: ", 100)
    email = input("Email (optional): ").strip() or None
    while True:
        pw = getpass.getpass("Password (min 6 chars): ")
        if len(pw) < 6:
            print("Password too short.")
            continue
        pw2 = getpass.getpass("Confirm password: ")
        if pw != pw2:
            print("Passwords don't match.")
            continue
        break
    try:
        u = create_user(username, pw, email)
        print("✅ Created user:", u.username)
    except Exception as e:
        print("Error:", e)

def cmd_login():
    global current_user
    print("\n--- Login ---")
    identifier = input_nonempty("Username or Email: ")
    pw = getpass.getpass("Password: ")
    u = authenticate_user(identifier, pw)
    if not u:
        print("Login failed: bad credentials.")
        return
    current_user = u
    print(f"✅ Logged in as {current_user.username}")

def cmd_logout():
    global current_user
    if current_user:
        print("Logged out:", current_user.username)
        current_user = None
    else:
        print("Not logged in.")

# ---------- CLI Commands ----------
def cmd_create_category():
    name = input_nonempty("Category name: ", 100)
    try:
        c = create_category(name)
        print("✅ Created category:", c.name)
    except Exception as e:
        print("Error:", e)

def cmd_add_expense():
    global current_user
    if not current_user:
        print("You must be logged in to add an expense.")
        return

    cats = list_categories()
    if not cats:
        print("No categories. Create one first.")
        return
    for i, c in enumerate(cats, 1):
        print(f" {i}) {c.name}")
    while True:
        choice = input(f"Choose category (1-{len(cats)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(cats):
            cat = cats[int(choice)-1]
            break
        print("Invalid choice.")
    name = input_nonempty("Expense name: ")
    amount = input_decimal("Amount (₹): ")
    e = create_expense(current_user.id, cat.id, name, amount)
    print(f"✅ Expense saved (id={e.id})")

def cmd_list_expenses():
    global current_user
    if not current_user:
        print("You must be logged in to list your expenses.")
        return
    exps = list_expenses(user_id=current_user.id)
    if not exps:
        print("No expenses found.")
        return
    print(f"\nExpenses for {current_user.username}:")
    for e in exps:
        print(f"ID:{e.id} | Category:{e.category.name} | {e.name} | ₹{float(e.amount):.2f} | Created:{e.created_at} | Updated:{e.updated_at}")

def cmd_update_expense():
    global current_user
    if not current_user:
        print("You must be logged in to update an expense.")
        return
    exps = list_expenses(user_id=current_user.id)
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
    global current_user
    if not current_user:
        print("You must be logged in to delete an expense.")
        return
    exps = list_expenses(user_id=current_user.id)
    if not exps:
        print("No expenses to delete.")
        return
    exp = exps[choose_from_list(exps, "expense")]
    confirm = input(f"Type 'yes' or 'y' to delete {exp.name}: ").strip().lower()
    if confirm in ("yes", "y"):
        delete_expense(exp.id)
        print("✅ Deleted.")
    else:
        print("Cancelled.")

# ---------- Graphing ----------
RANGES = {
    "1": ("7 days", 7),
    "2": ("30 days", 30),
    "3": ("3 months (90 days)", 90),
    "4": ("1 year (365 days)", 365),
}

def cmd_show_graph():
    global current_user
    if not current_user:
        print("You must be logged in to view graphs.")
        return
    print("\nChoose range:")
    for k, (label, _) in RANGES.items():
        print(f" {k}) {label}")
    choice = input("Choice: ").strip()
    if choice not in RANGES:
        print("Invalid choice.")
        return
    label, days = RANGES[choice]
    print(f"Generating graph for last {label}...")

    dates, totals = get_expense_aggregates_by_date(current_user.id, days)

    # Plot using matplotlib and save PNG
    # x labels as short "YYYY-MM-DD" strings
    x = [d.strftime("%Y-%m-%d") for d in dates]
    y = [float(t) for t in totals]

    plt.figure(figsize=(10, 4))
    plt.plot(x, y, marker='o')
    plt.title(f"Expenses for {current_user.username} — last {label}")
    plt.xlabel("Date")
    plt.ylabel("Total (₹)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    filename = f"expenses_{current_user.username}_{days}d.png"
    plt.savefig(filename)
    plt.close()
    print(f"Graph saved to {os.path.abspath(filename)}")

# ---------- Menu ----------
def show_menu():
    print("\n===== Expense Tracker =====")
    print("Auth:")
    print("  r) Register")
    print("  l) Login")
    print("  o) Logout")
    print("")
    print("Actions (login required):")
    print("  1) Create category")
    print("  2) Add expense")
    print("  3) List my expenses")
    print("  4) Update expense")
    print("  5) Delete expense")
    print("  6) Show expense graph")
    print("  0) Exit")

def main():
    init_db()
    while True:
        show_menu()
        c = input("Choose option: ").strip().lower()
        if c == "r": cmd_register()
        elif c == "l": cmd_login()
        elif c == "o": cmd_logout()
        elif c == "1": cmd_create_category()
        elif c == "2": cmd_add_expense()
        elif c == "3": cmd_list_expenses()
        elif c == "4": cmd_update_expense()
        elif c == "5": cmd_delete_expense()
        elif c == "6": cmd_show_graph()
        elif c == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
