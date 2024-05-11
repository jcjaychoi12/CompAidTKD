from sqlalchemy import Column, Integer, String, CHAR, Float, ForeignKey, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import get_session

Base = declarative_base()

class Teams(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    competitors = relationship("Competitors", back_populates="teams")

    @classmethod
    def new_Team(cls, name: str):
        with get_session() as session:
            new_team = cls(name=name)
            session.add(new_team)
            return new_team
        
    @classmethod
    def update_Team(cls, id: int, name: str):
        with get_session() as session:
            team = session.query(cls).filter(cls.id == id).first()

            if team is None:
                raise ValueError(f"No team found with ID {id}")
            
            setattr(team, "name", name)

    @classmethod
    def delete_Team(cls, id: int) -> None:
        with get_session() as session:
            del_team = delete(cls).where(cls.id == id)
            session.execute(del_team)

    @classmethod
    def get_Team(cls, id: int):
        with get_session() as session:
            return session.query(cls).filter(cls.id == id).first()