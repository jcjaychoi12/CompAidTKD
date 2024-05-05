from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Float, Boolean, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()
PG_URL = os.getenv("PG_URL")

# Configurations
Base = declarative_base()
engine = create_engine(PG_URL, echo=False)

# Tables
class Competitors(Base):
    __tablename__ = 'competitors'

    id = Column(Integer, primary_key=True)
    first_name = Column("firstName", String, nullable=False)
    last_name = Column("lastName", String, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False)

    def __repr__(self):
        return f"({self.last_name}, {self.first_name})"
    
# Upload tables into database
Base.metadata.create_all(bind=engine)

# Create Session
Session = sessionmaker(bind=engine)
session = Session()