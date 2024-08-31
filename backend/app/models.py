from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'    

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String, nullable=True)

    events = db.relationship("Event", back_populates="employee")

    def __repr__(self):
        return f'<Employee {self.name}, {self.email}, {self.phone_number}>'


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.DATE, nullable=False)  # Changed from TIMESTAMP to DATE
    hours = db.Column(db.Float, nullable=False)  # Renamed from duration to hours
    position = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    employee = db.relationship("Employee", back_populates="events")

    def __repr__(self):
        return (f'<Event name={self.name}, date={self.date}, hours={self.hours}, '
                f'position={self.position}, location={self.location}, '
                f'employee_id={self.employee_id}>')
# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy.types import Date

# Base = declarative_base()

# class Employee(Base):
#     __tablename__ = 'employees'
    
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     email = Column(String)

#     events = relationship("Event", back_populates="employee")

# class Event(Base):
#     __tablename__ = 'events'
    
#     id = Column(Integer, primary_key=True)
#     employee_id = Column(Integer, ForeignKey('employees.id'))
#     name = Column(String, nullable=False)
#     email = Column(String, nullable=False)
#     date = Column(String, nullable=False)
#     duration = Column(String, nullable=False)
#     position = Column(String, nullable=False)
#     location = Column(String, nullable=False)

#     employee = relationship("Employee", back_populates="events")
