from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import get_session

Base = declarative_base()

class Sparrings(Base):
    __tablename__ = "sparrings"
    # UniqueConstraint("attribute/column name", name="name of the constraint")
    # Allows one-to-one relatinship with Matches
    __table_args__ = (UniqueConstraint("mid", name="sparringPerMatch"),)

    mid = Column(Integer, ForeignKey("matches.id"), primary_key=True)
    cid1 = Column(Integer, ForeignKey("competitors.id"))
    cid2 = Column(Integer, ForeignKey("competitors.id"))
    winner = Column(Integer, nullable=False, default=-1)

    matches = relationship("Matches", back_populates="sparrings")

    @classmethod
    def new_Sparring(cls, mid: int, cid1: int, cid2: int):
        with get_session() as session:
            new_sparring = cls(mid=mid, cid1=cid1, cid2=cid2)
            session.add(new_sparring)
            return new_sparring
        
    @classmethod
    def update_Sparring(cls, mid: int, changes: dict):
        with get_session() as session:
            sparring = session.query(cls).filter(cls.mid == mid).first()

            if sparring is None:
                raise ValueError(f"No sparring match found with match ID {mid}")
            
            for key, value in changes.items():
                if hasattr(sparring, key):
                    setattr(sparring, key, value)
                else:
                    raise ValueError(f"Attribute {key} does not exist on Sparrings")
                
    @classmethod
    def delete_Sparring(cls, mid: int):
        with get_session() as session:
            del_sparring = delete(cls).where(cls.mid == mid)
            session.execute(del_sparring)

    @classmethod
    def get_Sparring(cls, mid: int):
        with get_session() as session:
            return session.query(cls).filter(cls.mid == mid).first()