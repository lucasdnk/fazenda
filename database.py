from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config import config

# Criar engine usando as configurações
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Modelos
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    salt = Column(String(16))
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime)
    active = Column(Integer, default=1)

class Farm(Base):
    __tablename__ = "farms"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200))
    created_at = Column(DateTime, default=datetime.now)
    fields = relationship("Field", back_populates="farm")

class Field(Base):
    __tablename__ = "fields"
    
    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey('farms.id'))
    name = Column(String(100), nullable=False)
    area = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    farm = relationship("Farm", back_populates="fields")
    crops = relationship("Crop", back_populates="field")
    activities = relationship("Activity", back_populates="field")

class Crop(Base):
    __tablename__ = "crops"
    
    id = Column(Integer, primary_key=True)
    field_id = Column(Integer, ForeignKey('fields.id'))
    crop_type = Column(String(50))
    planting_date = Column(DateTime)
    status = Column(String(20), default='active')
    created_at = Column(DateTime, default=datetime.now)
    field = relationship("Field", back_populates="crops")

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True)
    field_id = Column(Integer, ForeignKey('fields.id'))
    activity_type = Column(String(50))
    description = Column(String(500))
    status = Column(String(20), default='pending')
    created_at = Column(DateTime, default=datetime.now)
    field = relationship("Field", back_populates="activities")

# Criar todas as tabelas
def init_db():
    Base.metadata.create_all(engine)

# Obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 