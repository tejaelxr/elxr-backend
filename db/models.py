from sqlalchemy import Column, Date, Integer, String, DateTime, ForeignKey, LargeBinary, JSON
import sqlalchemy
from db.database import engine

Base = sqlalchemy.orm.declarative_base()

class Slider(Base):
    __tablename__ ='Slider'
    id = Column(Integer, primary_key=True,autoincrement=True)
    slide_name = Column(String(255))
    slide_type = Column(String(255))
    expiry_date = Column(Date)
    content = Column(LargeBinary)

class JobOpening(Base):
    __tablename__ = 'JobOpening'
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name=Column(String(252))
    opening_date=Column(Date)
    job_duties=Column(String(1000))
    location = Column(String(500))
    number_of_openings= Column(Integer)
    education_required = Column(String(500))
    experience_required = Column(String(500))
    
Base.metadata.create_all(bind=engine)