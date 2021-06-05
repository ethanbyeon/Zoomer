from sqlalchemy import create_engine
from sqlalchemy.orm import backref, declarative_base, relation, relationship, Session
import datetime

from sqlalchemy import (Boolean,
                        Column,
                        DateTime,
                        Integer,
                        ForeignKey,
                        String,
                        )
from sqlalchemy.sql.sqltypes import Boolean

Base = declarative_base()
engine = create_engine("sqlite:///")


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    first = Column(String(40), nullable=False)
    middle = Column(String(40))
    last = Column(String(40), nullable=False)
    leader_id = Column(Integer, ForeignKey("student.id"), nullable=True)
    
    leader = relationship("Student", remote_side=[id])

    def today(self):
        return list(filter(lambda x : x.date.date()==datetime.date.today(), self.attendance))[0]

    def __repr__(self):
        return (f'Student(id={self.id}, '
                f'first={self.first}, '
                f'middle={self.middle}, '
                f'last={self.last}, '
                f'leader_id={self.leader_id}, ')

    @property
    def serialize(self):
        return {'id': self.id, 
                'first': self.first,
                'middle': self.middle,
                'last': self.last,
                'leader_id': self.leader_id, 
                'status': self.today().status}



class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=lambda: datetime.datetime.now().replace(microsecond=0))
    status = Column(Boolean, default=False)
    student_id = Column(Integer, ForeignKey(Student.id))

    student = relationship("Student", backref="attendance")

    def __repr__(self):
        return (f'Attendance(id={self.id}, '
                f'date={self.date}, '
                f'status={self.status}, '
                f'student_id={self.student_id})')
    
    @property
    def serialize(self):
        return {'id': self.id, 
                'date': self.date,
                'status': self.status,
                'student_id': self.student_id }