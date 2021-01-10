from flask import Flask, request
from flask_restful import Resource, Api

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from control import *


app = Flask(__name__)
api = Api(app)

engine = create_engine('postgresql://postgres:1111@localhost/mydb', echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

if __name__=="__main__":

    api.add_resource(AddCourse, '/course')
    api.add_resource(UpdateCourse, '/course/<int:cid>')
    api.add_resource(GetCourse, '/course/<int:id>')
    api.add_resource(DeleteCourse, '/course/<int:cid>')

    api.add_resource(Addteacher, '/teach')
    api.add_resource(AddStudent, '/stud')
    api.add_resource(UpdateTeacher, '/teach/<int:id>')
    api.add_resource(UpdateStudent, '/stud/<int:id>')
    # api.add_resource(DeleteTeacher, '/teach/<int:id>')
    # api.add_resource(DeleteStudent, '/stud/<int:id>')
    api.add_resource(GetTeacher, '/teach/<int:id>')
    api.add_resource(GetStudent, '/stud/<int:id>')
    api.add_resource(GetAllUsers, '/allusers')
    api.add_resource(GetAllCourses,'/allcourses')

    api.add_resource(AddRequest, '/request/<int:cid>')
    api.add_resource(GetRequest, '/request/<int:id>')
    api.add_resource(UpdateReq, '/request/<int:id>')
    app.run(debug=True)
'''
 {
     "firstname": "Anton",
     "lastname": "Kovalenko",
     "email": "an@gmail.com",
     "password": "assddsd"
 }

{
     "firstname": "Maria",
     "lastname": "Ivanivna",
     "email": "MarIv@gmail.com",
     "password": "234fdvds"
 }

 {
     "name": "Math"
 }


 {
     "course_id":"1",
     "student_id":"2",
     "status":"no"
 }
'''