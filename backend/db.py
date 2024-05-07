from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Float, Boolean, CHAR, UniqueConstraint
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
    tid = Column (Integer, ForeignKey("teams.id")) # One-to-Many --> the Many table will take the foreign key

    # relatinship("Name of Class", back_populates="name of relationship variable in mentioned class")
    # Allows automatic changes to be propagated
    teams = relationship("Teams", back_populates="competitors")

    def __repr__(self):
        return f"({self.last_name}, {self.first_name})"
    
class Teams(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    competitors = relationship("Competitors", back_populates="teams")

class Matches(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    match_type = Column("type", CHAR, nullable=False)
    status = Column(String, nullable=False, default="not started")

    # uselist=False --> returns only one instance and not a list
    sparrings = relationship("Sparrings", back_populates="matches", uselist=False)
    poomsaes = relationship("Poomsaes", back_populates="matches")

class Sparrings(Base):
    __tablename__ = "sparrings"
    # UniqueConstraint("attribute/column name", name="name of the constraint")
    # Allows one-to-one relatinship with Matches
    __table_args__ = (UniqueConstraint("mid", name="sparringPerMatch"),)

    mid = Column(Integer, ForeignKey("matches.id"), primary_key=True)
    cid = Column(Integer, ForeignKey("competitors.id"))
    color = Column(String, nullable=False)
    winner = Column(Integer, nullable=False, default=-1)

    matches = relationship("Matches", back_populates="sparrings")

class Poomsaes(Base):
    __tablename__ = "poomsaes"

    mid = Column(Integer, ForeignKey("matches.id"))
    cid = Column(Integer, ForeignKey("competitors.id"))
    result = Column(Integer, nullable=False, default=-1)

    matches = relationship("Matches", back_populates="poomsaes")


# Upload tables into database
Base.metadata.create_all(bind=engine)


# Create Session
Session = sessionmaker(bind=engine)
session = Session()