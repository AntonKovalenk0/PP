from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    password = Column(String)
    status = Column(String)

    def __init__(self, firstname, lastname, email, password, status):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.status = status

#
# class Student(Base):
#     __tablename__ = "students"
#     id = Column(Integer, primary_key=True)
#     firstname = Column(String)
#     lastname = Column(String)
#     email = Column(String)
#     password = Column(String)
#
#     def __init__(self, firstname, lastname, email ,password):
#         self.firstname = firstname
#         self.lastname = lastname
#         self.email = email
#         self.password = password


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey(User.id))#, ForeignKey(Teacher.id))
    students_of_course = Column(Integer)


    def __init__(self, name, owner_id, students_of_course):
        self.name = name
        self.owner_id = owner_id
        self.students_of_course = students_of_course


class StudOnCourse(Base):
    __tablename__ = "stud_courses"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey(User.id))
    course_id = Column(Integer, ForeignKey(Course.id))#, ForeignKey(Teacher.id))

    def __init__(self, student_id,  course_id):
        self.student_id = student_id
        self. course_id = course_id



class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey(Course.id))# ForeignKey(Course.id))
    student_id = Column(Integer, ForeignKey(User.id))# ForeignKey(Student.id))
    status = Column(String)

    def __init__(self, course_id, student_id, status):
        self.course_id = course_id
        self.student_id = student_id
        self.status = status


# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True)
#     firstname = Column(String)
#     lastname = Column(String)
#     email = Column(String)
#     phone = Column(String)
#     status = Column(Integer)
#
#     def __init__(self, firstname, lastname, email, phone, status):
#         self.firstname = firstname
#         self.lastname = lastname
#         self.email = email
#         self.phone = phone
#         self.status = status