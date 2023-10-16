from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from models import Base

DATABASE_URL = 'sqlite:///game_data.db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def setup_database():
    try:
        Base.metadata.create_all(engine)
        print("Database set up successfully!")
    except SQLAlchemyError as e:
        print(f"An error occurred while setting up the database: {e}")

def get_session():
    """ Returns a new session for database operations """
    return SessionLocal()
