from sqlalchemy import Column, Integer, ForeignKey, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import get_session

Base = declarative_base()

class Poomsaes(Base):
    __tablename__ = "poomsaes"

    id = Column(Integer, primary_key=True)
    mid = Column(Integer, ForeignKey("matches.id"))
    cid = Column(Integer, ForeignKey("competitors.id"))
    result = Column(Integer, nullable=False, default=-1)

    matches = relationship("Matches", back_populates="poomsaes")

    @classmethod
    def new_Poomsae(cls, mid: int, cid: int):
        with get_session() as session:
            new_poomsae = cls(mid=mid, cid=cid)
            session.add(new_poomsae)
            return new_poomsae
        
    @classmethod
    def update_Poomsae(cls, mid: int, changes: dict):
        with get_session() as session:
            poomsae = session.query(cls).filter(cls.mid == mid).first()

            if poomsae is None:
                raise ValueError(f"No poomsae match found with match ID {mid}")
            
            for key, value in changes.items():
                if hasattr(poomsae, key):
                    setattr(poomsae, key, value)
                else:
                    raise ValueError(f"Attribute {key} does not exist on Poomsaes")
                
    @classmethod
    def delete_Poomsae(cls, mid: int, cid: int):
        with get_session() as session:
            del_Poomsae = delete(cls).where(cls.mid == mid and cls.cid == cid)
            session.execute(del_Poomsae)

    @classmethod
    def get_Poomsae(cls, mid: int, cid: int):
        with get_session() as session:
            return session.query(cls).filter(cls.mid == mid and cls.cid == cid).first()