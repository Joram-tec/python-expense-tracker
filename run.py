# run.py
# Creates tables, launches CLI
from database import Base, engine
from . import models  # ensures models are registered

# Create the database tables
Base.metadata.create_all(engine)

# Start the CLI
from cli import main_menu
main_menu()
