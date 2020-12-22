from flask import Flask
from flask_restful import Resource, Api

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from control import *


app = Flask(__name__)
api = Api(app)

engine = create_engine('postgresql://postgres:1234@localhost/db11', echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

if __name__=="__main__":

    api.add_resource(AddCourse, '/teach/course')
    api.add_resource(UpdateCourse, '/teach/course/<int:id>')
    api.add_resource(GetCourse, '/course/<int:id>')
    api.add_resource(DeleteCourse, '/course/<int:id>')

    api.add_resource(Addteacher, '/teach')
    api.add_resource(AddStudent, '/stud')
    api.add_resource(UpdateTeacher, '/teach/<int:id>')
    api.add_resource(UpdateStudent, '/stud/<int:id>')
    api.add_resource(DeleteTeacher, '/teach/<int:id>')
    api.add_resource(DeleteStudent, '/stud/<int:id>')
    api.add_resource(GetTeacher, '/teach/<int:id>')
    api.add_resource(GetStudent, '/stud/<int:id>')
    api.add_resource(GetAllStud, '/allst')

    api.add_resource(AddRequest, '/request')
    api.add_resource(GetRequest, '/request/<int:id>')
    api.add_resource(UpdateReq, '/request/<int:id>')
    app.run(debug=True)
'''
 {
     "firstname": "Anton",
     "lastname": "Kovalenko",
     "password": "assddsd"
 }


 {
     "name": "Math",
     "owner_id": "7",
     "students_of_course": "5",
     "status": "1"
 }


 {
     "course_id":"1",
     "student_id":"2",
     "status":"no"
 }
'''