from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, delete, ForeignKey, Column, String, Integer, Float, CHAR, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from contextlib import contextmanager


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


# Models
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
            return new_user.json()
        
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
            return session.query(cls).filter(cls.id == id).first().json()
        
    def json(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "gender": self.gender,
            "age": self.age,
            "weight": self.weight,
            "height": self.height,
            "rank": self.rank,
            "tid": self.tid
        }

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
            return new_team.json()
        
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
            return session.query(cls).filter(cls.id == id).first().json()

    def json(self):
        return {
            "id": self.id,
            "name": self.name
        }

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
            return new_match.json()
        
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
            return session.query(cls).filter(cls.id == id).first().json()

    def json(self):
        return {
            "id": self.id,
            "type": self.match_type,
            "status": self.status
        }

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
            return new_sparring.json()
        
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
            return session.query(cls).filter(cls.mid == mid).first().json()
        
    def json(self):
        return {
            "mid": self.mid,
            "cid1": self.cid1,
            "cid2": self.cid2,
            "winner": self.winner
        }

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


# Upload tables into database
Base.metadata.create_all(bind=engine)
