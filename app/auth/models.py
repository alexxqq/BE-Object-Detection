from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base, engine

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Integer, default=True)

    tasks = relationship('Task', back_populates='user')


Base.metadata.create_all(bind=engine)
