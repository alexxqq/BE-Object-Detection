from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base, engine

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    status = Column(String)
    result = Column(String, nullable=True)
    error = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='tasks')
    results = relationship('TaskResult', back_populates='task', cascade='all, delete')

    def __repr__(self):
        return f"<Task(id={self.id}, task_id='{self.task_id}', status='{self.status}', user_id={self.user_id})>"

class TaskResult(Base):
    __tablename__ = 'task_results'

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    name = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)

    task = relationship('Task', back_populates='results')

    def __repr__(self):
        return f"<TaskResult(id={self.id}, task_id={self.task_id}, name='{self.name}', confidence={self.confidence})>"


Base.metadata.create_all(bind=engine)
