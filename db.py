from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import hashlib

# Create a SQLite database (you can replace 'sqlite:///users.db' with another database URL, e.g., for PostgreSQL)
engine = create_engine('sqlite:///users.db')  # echo=True for logging, remove in production

# Create a base class for declarative models
class Base(DeclarativeBase):
    pass

# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # Store hashed password for security
    email = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<User(username='{self.username}',hashed_password='{self.hashed_password}', email='{self.email}')>"

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()
