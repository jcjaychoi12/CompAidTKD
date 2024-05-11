from sqlalchemy import Column, Integer, String, CHAR, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import get_session

Base = declarative_base()

class Matches(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    match_type = Column("type", CHAR, nullable=False)
    status = Column(String, nullable=False, default="not started")

    # uselist=False --> returns only one instance and not a list
    sparrings = relationship("Sparrings", back_populates="matches", uselist=False)
    poomsaes = relationship("Poomsaes", back_populates="matches")

    @classmethod
    def new_Match(cls, match_type: str):
        with get_session() as session:
            match_type = match_type.lower()
            if match_type in ["s", "sparring"]:
                match_type = "s"
            elif match_type in ["p", "poomsae"]:
                match_type = "p"
            else:
                raise ValueError(f"Invalid match type: {match_type} --> Value must be s/sparring or p/poomsae")

            new_match = cls(match_type=match_type)
            session.add(new_match)
            return new_match
        
    @classmethod
    def update_Match(cls, id: int, match_type: str):
        with get_session() as session:
            match = session.query(cls).filter(cls.id == id).first()

            if match is None:
                raise ValueError(f"No match found with ID {id}")
            
            match_type = match_type.lower()
            if match_type in ["s", "sparring"]:
                match_type = "s"
            elif match_type in ["p", "poomsae"]:
                match_type = "p"
            else:
                raise ValueError(f"Invalid match type: {match_type} --> Value must be s/sparring or p/poomsae")

            
            setattr(match, "match_type", match_type[0])

    @classmethod
    def delete_Match(cls, id: int):
        with get_session() as session:
            del_match = delete(cls).where(cls.id == id)
            session.execute(del_match)

    @classmethod
    def get_Match(cls, id: int):
        with get_session() as session:
            return session.query(cls).filter(cls.id == id).first()