from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:1234@localhost/mydb", echo=True)

Session = sessionmaker(bind=engine)
Base = declarative_base()


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column('id', Integer, primary_key=True)
    firstname = Column('firstname', String)
    lastname = Column('lastname', String)
    password = Column('password', String)


class Student(Base):
    __tablename__ = "students"

    id = Column('id', Integer, primary_key=True)
    firstname = Column('firstname', String)
    lastname = Column('lastname', String)
    password = Column('password', String)


class Course(Base):
    __tablename__ = "courses"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    owner_id = Column('owner_id', Integer, ForeignKey(Student.id))
    students_of_course = Column('students_of_course', Integer)
    status = Column('status', Integer)


class Request(Base):
    __tablename__ = "requests"

    id = Column('id', Integer, primary_key=True)
    course_id = Column('course_id', Integer, ForeignKey(Course.id))
    student_id = Column('student_id', Integer, ForeignKey(Student.id))



class User(Base):
    __tablename__ = "users"

    id = Column('id', Integer, primary_key=True)
    firstname = Column('firstname', String)
    lastname = Column('lastname', String)
    email = Column('email', String)
    phone = Column('phone', String)
    status = Column('status', Integer)


