from database import session
from models import Expense, User, Category
from datetime import datetime

def get_or_create_user(name):
    user = session.query(User).filter_by(name=name).first()
    if not user:
        user = User(name=name, email=f"{name.lower()}@example.com")
        session.add(user)
        session.commit()
    return user

def get_or_create_category(name):
    category = session.query(Category).filter_by(name=name).first()
    if not category:
        category = Category(name=name)
        session.add(category)
        session.commit()
    return category

def add_expense(amount, description, date, user_id, category_id):
    user = session.query(User).get(user_id)
    category = session.query(Category).get(category_id)

    if not user:
        print(" User not found. Please try again.")
        return

    if not category:
        print(" Category not found. Please try again.")
        return

    expense = Expense(amount=amount, description=description, date=date, user=user, category=category)
    session.add(expense)
    session.commit()
    print(" Expense added successfully.")


def view_expenses():
    return session.query(Expense).order_by(Expense.date.desc()).all()

def create_user(name, email):
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    return user

def create_category(name):
    category = Category(name=name)
    session.add(category)
    session.commit()
    return category

def get_all_users():
    return session.query(User).all()

def get_all_categories():
    return session.query(Category).all()

def filter_expenses_by_category(category_id):
    return session.query(Expense).filter_by(category_id=category_id).order_by(Expense.date.desc()).all()

def filter_expenses_by_category_name(category_name):
    category = session.query(Category).filter_by(name=category_name).first()
    if not category:
        return []
    return session.query(Expense).filter_by(category_id=category.id).order_by(Expense.date.desc()).all()

def filter_expenses_by_date(start_date_str, end_date_str):
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

    return session.query(Expense).filter(
        Expense.date >= start_date,
        Expense.date <= end_date
    ).order_by(Expense.date.desc()).all()

def delete_user_by_name(name):
    user = session.query(User).filter(User.name.ilike(name)).first()
    if user:
        session.delete(user)
        session.commit()
        print(f"User '{user.name}' deleted successfully.")
    else:
        print("User not found.")

def delete_expense_by_description(description):
    expense = session.query(Expense).filter(Expense.description.ilike(description)).first()
    if expense:
        session.delete(expense)
        session.commit()
        print(f"Expense '{expense.description}' deleted successfully.")
    else:
        print("Expense not found.")
def update_expense(expense_id, amount=None, description=None, date_str=None, user_name=None, category_name=None):
    expense = session.query(Expense).filter_by(id=expense_id).first()
    if not expense:
        raise ValueError("Expense not found.")

    if amount is not None:
        expense.amount = amount
    if description is not None:
        expense.description = description
    if date_str is not None:
        try:
            expense.date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format.")
    if user_name is not None:
        expense.user = get_or_create_user(user_name)
    if category_name is not None:
        expense.category = get_or_create_category(category_name)

    session.commit()
