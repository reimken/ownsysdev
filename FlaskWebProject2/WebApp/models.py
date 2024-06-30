from WebApp import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class Manager(db.Model):
    __tablename__ = 'managers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    
    '''def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password_hash, password)

    #tasks = db.relationship('Task', backref='manager', lazy=True)'''

    def __repr__(self):
        return f"<Manager(id={self.id}, name='{self.name}', email='{self.email}')>"

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    type_id = db.Column(db.Integer, nullable=False)

    #tasks = db.relationship('Task', backref='project', lazy=True)

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', description='{self.description}', type_id={self.type_id})>"

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('managers.id'), nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Task(id={self.id}, name='{self.name}', description='{self.description}', project_id={self.project_id}, user_id={self.user_id}, deadline={self.deadline})>"
    
class Developer(db.Model):
    __tablename__ = 'developers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))

    def __repr__(self):
        return f"<Developer(id={self.id}, name='{self.name}', email='{self.email}')>"