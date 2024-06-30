from WebApp import db

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Manager(Base):
    __tablename__ = 'managers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    def __repr__(self):
        return f"<Manager(id={self.id}, name='{self.name}', email='{self.email}')>"

class Developer(Base):
    __tablename__ = 'developers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    def __repr__(self):
        return f"<Developer(id={self.id}, name='{self.name}', email='{self.email}')>"
    
class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    type_id = Column(Integer, ForeignKey('project_types.id'))
    description = Column(String(255))
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', type_id={self.type_id}, description='{self.description}')>"

class ProjectType(Base):
    __tablename__ = 'project_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    def __repr__(self):
        return f"<ProjectType(id={self.id}, name='{self.name}')>"
    
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    project_id = Column(Integer, ForeignKey('projects.id'))
    user_id = Column(Integer, ForeignKey('managers.id'))
    deadline = Column(DateTime)
    
    project = relationship("Project", back_populates="tasks")
    user = relationship("Manager", back_populates="tasks")
    
    def __repr__(self):
        return f"<Task(id={self.id}, name='{self.name}', project_id={self.project_id}, user_id={self.user_id}, deadline='{self.deadline}')>"

