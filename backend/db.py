from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, delete, ForeignKey, Column, String, Integer, Float, CHAR, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from contextlib import contextmanager
from models import Competitors, Teams, Matches, Sparrings, Poomsaes


# Load environment variables
load_dotenv()
PG_URL = os.getenv("PG_URL")


# Configurations
Base = declarative_base()
engine = create_engine(PG_URL, echo=False)


# Create session manager
Session = sessionmaker(bind=engine)


# Context manager = allows safer control of DB calls
@contextmanager
def get_session():
    session = Session()
    try: 
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


# Upload tables into database
Base.metadata.create_all(bind=engine)
