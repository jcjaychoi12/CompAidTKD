from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Float, Boolean, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


# Load environment variables
load_dotenv()
PG_URL = os.getenv("PG_URL")


# Configurations
Base = declarative_base()
engine = create_engine(PG_URL, echo=False)


# Tables
class Competitors(Base):
    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True)
    first_name = Column("firstName", String, nullable=False)
    last_name = Column("lastName", String, nullable=False)
    gender = Column(CHAR, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False)

    team = relationship("Teams", back_populates="competitor")

    def __repr__(self):
        return f"({self.last_name}, {self.first_name})"
    
class Teams(Base):
    __tablename__ = "teams"

    cid = Column(Integer, ForeignKey("competitors.id"))
    name = Column(String, nullable=False)

    competitor = relationship("Competitors", back_populates="team")


# Upload tables into database
Base.metadata.create_all(bind=engine)


# Create Session
Session = sessionmaker(bind=engine)
session = Session()