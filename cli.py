from datetime import datetime
from services import (
    create_user, create_category, add_expense,
    get_all_users, get_all_categories, view_expenses,
    filter_expenses_by_category, filter_expenses_by_date,
    update_expense
)

def main_menu():
    print("=== Welcome to the Personal Expense Tracker ===")

    while True:
        print("What do you want to do?")
        print("1. Add User")
        print("2. Add Category")
        print("3. Add Expense")
        print("4. View All Expenses")
        print("5. Filter Expenses by Category")
        print("6. Filter Expenses by Date")
        print("7. Update an Expense")
        print("8. Exit")

        choice = input("Enter choice (1-8): ")

        if choice == "1":
            name = input("Enter user's name: ")
            email = input("Enter user's email: ")
            create_user(name, email)
            print(" User added.")

        elif choice == "2":
            name = input("Enter category name: ")
            create_category(name)
            print(" Category added.")

        elif choice == "3":
            amount = float(input("Enter amount (e.g. 1200): "))
            description = input("Enter description: ")
            date_str = input("Enter date (YYYY-MM-DD): ")
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()  
            except ValueError:
                print(" Invalid date format. Please use YYYY-MM-DD.")

            users = get_all_users()
            print("\nUsers:")
            for u in users:
                print(f"- {u.name} ({u.email})")
            email = input("Enter your email: ")
            user = next((u for u in users if u.email == email), None)
            if not user:
                print(" User not found.")
                continue

            categories = get_all_categories()
            print("\nCategories:")
            for c in categories:
                print(f"- {c.name}")
            cat_name = input("Enter category name: ")
            category = next((c for c in categories if c.name.lower() == cat_name.lower()), None)
            if not category:
                print(" Category not found.")
                continue

            add_expense(amount, description, date, user.id, category.id)
            print(" Expense added.")

        elif choice == "4":
            expenses = view_expenses()
            if not expenses:
                print("No expenses found.")
            for exp in expenses:
                print(f"[{exp.id}] {exp.date} - {exp.amount} KES - {exp.description}")

        elif choice == "5":
            category_name = input("Enter category name to filter by: ")
            expenses = filter_expenses_by_category(category_name)
            if not expenses:
                print("No expenses in that category.")
            for exp in expenses:
                print(f"{exp.date} - {exp.amount} KES - {exp.description}")

        elif choice == "6":
            start = input("Start date (YYYY-MM-DD): ")
            end = input("End date (YYYY-MM-DD): ")
            expenses = filter_expenses_by_date(start, end)
            if not expenses:
                print("No expenses in that range.")
            for exp in expenses:
                print(f"{exp.date} - {exp.amount} KES - {exp.description}")

        elif choice == "7":
            expense_id = int(input("Enter Expense ID to update: "))
            new_amount = float(input("New amount: "))
            new_desc = input("New description: ")
            update_expense(expense_id, new_amount, new_desc)
            print("Expense updated.")

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print(" Invalid choice. Try again.")
