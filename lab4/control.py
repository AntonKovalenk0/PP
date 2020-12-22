from flask import json, Response, request
from flask_restful import Resource, Api
from models import *
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.ext.declarative import DeclarativeMeta

from app import session


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

class AddCourse(Resource):
    def post(self):
        data = request.json
        try:
            course = Course(data["name"],data["owner_id"],data["students_of_course"],data["status"])
            session.add(course)
            session.flush()
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )

class UpdateCourse(Resource):
    def put(self, id):
        data = request.json
        try:
            course1 = session.query(Course).get(id)
            if "name" in data:
                course1.name = data["name"]
            if "owner_id" in data:
                course1.owner_id = data['owner_id']
            if "students_of_course" in data:
                course1.students_of_course = data["students_of_course"]
            if "status" in data:
                course1.status = data["status"]
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )



class GetCourse(Resource):
    def get(self, id):
        course = session.query(Course).get(id)
        if course:
            return Response(
                response=json.dumps(course, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=404,
                mimetype="application/json"
            )
class DeleteCourse(Resource):
    def delete(self, id):
        course = session.query(Course).filter(Course.id==id).delete()
        session.commit()
        if course:
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=404,
                mimetype="application/json"
            )

class Addteacher(Resource):
    def post(self):
        data = request.json
        try:
            teacher = Teacher(data["firstname"],data["lastname"],data["password"])
            teacher.password = generate_password_hash(data['password'])
            session.add(teacher)
            session.flush()
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )

class AddStudent(Resource):
    def post(self):
        data = request.json
        try:
            student = Student(data["firstname"],data["lastname"],data["password"])
            student.password = generate_password_hash(data['password'])
            session.add(student)
            session.flush()
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )

class UpdateTeacher(Resource):
    def put(self, id):
        data = request.json
        try:
            teacher = session.query(Teacher).get(id)
            if "firstname" in data:
                teacher.firstname = data["firstname"]
            if "lastname" in data:
                teacher.lastname = data["lastname"]

            if "password" in data:
                teacher.password = data["password"]
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )


class UpdateStudent(Resource):
    def put(self, id):
        data = request.json
        try:
            student = session.query(Student).get(id)
            if "firstname" in data:
                student.firstname = data["firstname"]
            if "lastname" in data:
                student.lastname = data["lastname"]

            if "password" in data:
                student.password = data["password"]
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )


class GetTeacher(Resource):
    def get(self, id):
        user = session.query(Teacher).get(id)
        if user:
            return Response(
                response=json.dumps(user, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=400,
                mimetype="application/json"
            )

class GetStudent(Resource):
    def get(self, id):
        user = session.query(Student).get(id)
        if user:
            return Response(
                response=json.dumps(user, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=400,
                mimetype="application/json"
            )

class DeleteTeacher(Resource):
    def delete(self, id):
        user = session.query(Teacher).filter(Teacher.id==id).delete()
        session.commit()
        if user:
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=400,
                mimetype="application/json"
            )

class DeleteStudent(Resource):
    def delete(self, id):
        user = session.query(Student).filter(Student.id==id).delete()
        session.commit()
        if user:
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=400,
                mimetype="application/json"
            )
class GetAllStud(Resource):
    def get(self):
        student = session.query(Student).all()
        if student:
            return Response(
                response=json.dumps(student, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=404,
                mimetype="application/json"
            )
class AddRequest(Resource):
    def post(self):
        data = request.json
        try:
            req = Request(data["course_id"],data["student_id"],data["status"])
            session.add(req)
            session.flush()
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )

class GetRequest(Resource):
    def get(self, id):
        req = session.query(Request).get(id)
        if req:
            return Response(
                response=json.dumps(req, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=404,
                mimetype="application/json"
            )
class UpdateReq(Resource):
    def put(self, id):
        data = request.json
        try:
            req = session.query(Request).get(id)
            if "status" in data:
                req.status = data["status"]
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )