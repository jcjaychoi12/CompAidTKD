from sqlalchemy import Column, Integer, String, CHAR, Float, ForeignKey, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import get_session

Base = declarative_base()

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
    
    @classmethod
    def new_Competitor(cls, fname: str, lname: str, gender: str, age: int, height: float, weight: float, rank: int, tid: int):
        with get_session() as session:
            gender = gender.lower()
            if gender in ["m", "male", "man"]:
                gender = "m"
            elif gender in ["f", "female", "woman"]:
                gender = "f"
            else:
                raise ValueError(f"Invalid match type: {gender} --> Value must be m/male/man or f/female/woman")

            new_user = cls(
                first_name=fname,
                last_name=lname,
                gender=gender,
                age=age,
                height=height,
                weight=weight,
                rank=rank,
                tid=tid
            )
            session.add(new_user)
            return new_user
        
    @classmethod
    def update_Competitor(cls, id: int, changes: dict):
        with get_session() as session:
            if "gender" in changes:
                new_gender = changes.get("gender").lower()
                if new_gender in ["m", "male", "man"]:
                    new_gender = "m"
                elif new_gender in ["f", "female", "woman"]:
                    new_gender = "f"
                else:
                    raise ValueError(f"Invalid match type: {changes["gender"]} --> Value must be m/male/man or f/female/woman")
                changes["gender"] = new_gender

            competitor = session.query(cls).filter(cls.id == id).first()
            
            if competitor is None:
                raise ValueError(f"No competitor found with ID {id}")
            
            for key, value in changes.items():
                if hasattr(competitor, key):
                    setattr(competitor, key, value)
                else:
                    raise ValueError(f"Attribute {key} does not exist on Competitors")
                
    @classmethod
    def delete_Competitor(cls, id: int):
        with get_session() as session:
            del_competitor = delete(cls).where(cls.id == id)
            session.execute(del_competitor)

    @classmethod
    def get_Competitor(cls, id: int):
        with get_session() as session:
            return session.query(cls).filter(cls.id == id).first()