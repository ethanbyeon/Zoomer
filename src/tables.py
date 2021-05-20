from sqlalchemy import create_engine
from sqlalchemy.orm import backref, declarative_base, relationship, Session
import datetime

from sqlalchemy import (Column,
                        DateTime,
                        Integer,
                        ForeignKey,
                        String,
                        )

Base = declarative_base()
engine = create_engine("sqlite:///")

class Leader(Base):
    __tablename__ = "leader"

    id = Column(Integer, primary_key=True)
    last = Column(String(40), nullable=False)
    first = Column(String(40), nullable=False)
    middle = Column(String(40))
    students = relationship("Student", backref="leader", lazy=True)

    def __repr__(self):
        return (f'Leader(id={self.id}, '
                f'last={self.last}, ' 
                f'first={self.first}, ' 
                f'middle={self.middle})')


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    last = Column(String(40), nullable=False)
    first = Column(String(40), nullable=False)
    middle = Column(String(40))
    leader_id = Column(Integer, ForeignKey('leader.id'), nullable=True)

    def __repr__(self):
        return (f'Student(id={self.id}, '
                f'last={self.last}, '
                f'first={self.first}, '
                f'middle={self.middle}, '
                f'leader_id={self.leader_id})')


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    status = Column(String(40))
    leader_id = Column(Integer, ForeignKey('leader.id'), nullable=True)

    def __repr__(self):
        return (f'Attendance(id={self.id}, '
                f'date={self.date}, '
                f'status={self.status}, '
                f'leader_id={self.leader_id})')