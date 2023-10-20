# Import necessary modules from the SQLAlchemy library.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Import the Base class from the models module.
from models import Base

# Define the database URL.
DATABASE_URL = 'sqlite:///game.db'

# Create an engine to manage connections to the database.
engine = create_engine(DATABASE_URL)

# Create a sessionmaker that will serve as a factory for creating new sessions.
SessionLocal = sessionmaker(bind=engine)

def setup_database():
    """Set up the database by creating the necessary tables."""
    try:
        # Create all tables defined in the Base class (metadata).
        Base.metadata.create_all(engine)
        print("Database set up successfully!")
    except SQLAlchemyError as e:
        # Catch and print any errors that occur during database setup.
        print(f"An error occurred while setting up the database: {e}")

def get_session():
    """Returns a new session for database operations."""
    return SessionLocal()
