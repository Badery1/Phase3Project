from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)  # Made name unique for differentiation
    temperature = Column(Float, default=40.0)
    logs = Column(Integer, default=0)
    days_survived = Column(Integer, default=0)
    alive = Column(Boolean, default=True)  # True means alive, False means dead
    gathering_attempts = Column(Integer, default=3)
    logs_gathered = relationship("LogGathered", backref="player")

class LogGathered(Base):
    __tablename__ = 'logs_gathered'

    id = Column(Integer, primary_key=True)
    day = Column(Integer)
    logs = Column(Integer)  # Number of logs gathered on that day
    player_id = Column(Integer, ForeignKey('players.id'))

engine = create_engine('sqlite:///game.db')
Base.metadata.create_all(engine)
