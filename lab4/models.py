from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column('id', Integer, primary_key=True)
    firstname = Column('firstname', String)
    lastname = Column('lastname', String)
    password = Column('password', String)

    def __init__(self, firstname, lastname, password):
        self.firstname = firstname
        self.lastname = lastname
        self.password = password

class Student(Base):
    __tablename__ = "students"
    id = Column('id', Integer, primary_key=True)
    firstname = Column('firstname', String)
    lastname = Column('lastname', String)
    password = Column('password', String)

    def __init__(self, firstname, lastname, password):
        self.firstname = firstname
        self.lastname = lastname
        self.password = password

class Course(Base):
    __tablename__ = "courses"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    owner_id = Column('owner_id', String)#, ForeignKey(Teacher.id))
    students_of_course = Column('students_of_course', String)
    status = Column('status', String)

    def __init__(self, name, owner_id, students_of_course, status):
        self.name = name
        self.owner_id = owner_id
        self.students_of_course = students_of_course
        self.status = status
class Request(Base):
    __tablename__ = "requests"

    id = Column('id', Integer, primary_key=True)
    course_id = Column('course_id', Integer)# ForeignKey(Course.id))
    student_id = Column('student_id', Integer)# ForeignKey(Student.id))
    status = Column('status', String)

    def __init__(self, course_id, student_id, status):
        self.course_id = course_id
        self.student_id = student_id
        self.status = status

class User(Base):
    __tablename__ = "users"

    id = Column('id', Integer, primary_key=True)
    firstname = Column('firstname', String)
    lastname = Column('lastname', String)
    email = Column('email', String)
    phone = Column('phone', String)
    status = Column('status', Integer)


    def __init__(self, firstname, lastname, email, phone, status):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.status = status
