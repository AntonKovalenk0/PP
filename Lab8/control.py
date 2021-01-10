from flask import json, Response, request
from flask_restful import Resource, Api
from models import *
from flask_httpauth import HTTPBasicAuth
from functools import wraps
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



auth = HTTPBasicAuth()


@auth.verify_password
def verify_passsword(username,password):
    #session = Session()
    user = session.query(User).filter_by(email=username).first()
    if user:
        if check_password_hash(user.password,password):
            return user
        else:
            user = None
            return user
    else:
        user = None
        return user




class AddCourse(Resource):

    @auth.login_required

    def post(self):
        user = auth.current_user()
        if user == None:
            return Response(
                response=json.dumps({"message": "Wrong login or password"}),
                status=401,
                mimetype="application/json"
            )
        elif user.status != 'teacher':
            return  Response(
                response=json.dumps({"message": "You are not teacher"}),
                status=200,
                mimetype="application/json"
            )
        data = request.json

        try:
            course = Course(data["name"], user.id, 0)
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
    @auth.login_required

    def put(self, cid):
        user = auth.current_user()
        if user == None:
            return Response(
                response=json.dumps({"message": "Wrong login or password"}),
                status=401,
                mimetype="application/json"
            )
        elif user.status != 'teacher':
            return Response(
                response=json.dumps({"message": "You are not teacher"}),
                status=200,
                mimetype="application/json"
            )
        data = request.json
        try:
            course1 = session.query(Course).get(cid)

            if(user.id!=course1.owner_id):
                return Response(
                    response=json.dumps({"message": "You are not owner of this course!"}),
                    status=401,
                    mimetype="application/json"
                )
            else:
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
    @auth.login_required
    def delete(self, cid):
        user = auth.current_user()
        if user == None:
            return Response(
                response=json.dumps({"message": "Wrong login or password"}),
                status=401,
                mimetype="application/json"
            )
        elif user.status != 'teacher':
            return Response(
                response=json.dumps({"message": "You are not teacher"}),
                status=200,
                mimetype="application/json"
            )
        else:
            course1 = session.query(Course).get(cid)

            if (user.id != course1.owner_id):
                return Response(
                    response=json.dumps({"message": "You are not owner of this course!"}),
                    status=401,
                    mimetype="application/json"
                )
        # course1 = session.query(Course).get(cid)
        # if (tid != course1.owner_id):
        #     return Response(
        #         response=json.dumps({"message": "You are not owner of this course!"}),
        #         status=401,
        #         mimetype="application/json"
        #     )
        session.query(Request).filter(Request.course_id == cid).delete()
        session.query(StudOnCourse).filter(Course.id == cid).delete()
        course = session.query(Course).filter(Course.id==cid).delete()
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

class GetAllCourses(Resource):
    def get(self):
        courses = session.query(Course).all()
        if courses:
            return Response(
                response=json.dumps(courses, cls=AlchemyEncoder),
                status=201,
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
            teacher = User(data["firstname"],data["lastname"],data["email"], data["password"],"teacher")
            teacher.password = generate_password_hash(data['password'])
            user = session.query(User).filter_by(email=data["email"]).first()
            if user == None:


                session.add(teacher)
                session.flush()
                session.commit()
                return Response(
                    response=json.dumps({"message": "Success"}),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=json.dumps({"message": "Email is already exist"}),
                    status=401,
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
            user = session.query(User).filter_by(email=data["email"]).first()
            if user == None:
                student = User(data["firstname"],data["lastname"],data["email"],data["password"], "student")
                student.password = generate_password_hash(data['password'])
                session.add(student)
                session.flush()
                session.commit()
                return Response(
                    response=json.dumps({"message": "Success"}),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=json.dumps({"message": "Email is already exist"}),
                    status=401,
                    mimetype="application/json"
                )
        except:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )


class UpdateTeacher(Resource):
    @auth.login_required

    def put(self, id):
        user = auth.current_user()
        if (id != user.id):
            return Response(
                response=json.dumps({"message": "You cannot update!"}),
                status=401,
                mimetype="application/json"
            )
        if user == None:
            return Response(
                response=json.dumps({"message": "Wrong login or password"}),
                status=401,
                mimetype="application/json"
            )
        elif user.status != 'teacher':
            return Response(
                response=json.dumps({"message": "You are not teacher"}),
                status=200,
                mimetype="application/json"
            )
        data = request.json
        try:
            teacher = session.query(User).get(id)
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
    @auth.login_required


    def put(self, id):
        user = auth.current_user()
        if (id != user.id):
            return Response(
                response=json.dumps({"message": "You cannot update!"}),
                status=401,
                mimetype="application/json"
            )
        if user == None:
            return Response(
                response=json.dumps({"message": "Wrong login or password"}),
                status=401,
                mimetype="application/json"
            )
        elif user.status != 'student':
            return Response(
                response=json.dumps({"message": "You are not student"}),
                status=200,
                mimetype="application/json"
            )
        data = request.json
        try:
            student = session.query(User).get(id)
            if "firstname" in data:
                student.firstname = data["firstname"]
            if "lastname" in data:
                student.lastname = data["lastname"]

            if "password" in data:
                student.password = generate_password_hash(data['password'])
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
        user = session.query(User).get(id)
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
        user = session.query(User).get(id)
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
        user = session.query(User).filter(User.id==id).delete()
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
    @auth.login_required
    def delete(self, id):
        user = auth.current_user()
        if (id != user.id):
            return Response(
                response=json.dumps({"message": "You cannot update!"}),
                status=401,
                mimetype="application/json"
            )
        if user == None:
            return Response(
                response=json.dumps({"message": "Wrong login or password"}),
                status=401,
                mimetype="application/json"
            )
        elif user.status != 'student':
            return Response(
                response=json.dumps({"message": "You are not student"}),
                status=200,
                mimetype="application/json"
            )

        user = session.query(User).filter(User.id==id).delete()
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


class GetAllUsers(Resource):
    def get(self):
        student = session.query(User).all()
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
    @auth.login_required

    def post(self, cid):
        user = auth.current_user()
        if user == None:
            return Response(
                response=json.dumps({"message": "Wrong login or password"}),
                status=401,
                mimetype="application/json"
            )
        elif user.status != 'student':
            return Response(
                response=json.dumps({"message": "You are not student"}),
                status=200,
                mimetype="application/json"
            )
        try:
            req = Request(cid,user.id,"no")
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
    @auth.login_required

    def get(self, id):

        user = auth.current_user()
        if user == None:
            return Response(
                response=json.dumps({"message": "Wrong login or password"}),
                status=401,
                mimetype="application/json"
            )
        elif user.status != 'teacher':
            return Response(
                response=json.dumps({"message": "You are not teacher"}),
                status=200,
                mimetype="application/json"
            )
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
    @auth.login_required

    def put(self, id):
        user = auth.current_user()
        if user == None:
            return Response(
                response=json.dumps({"message": "Could not verify your login"}),
                status=401,
                mimetype="application/json"
            )
        elif user.status != 'teacher':
            return Response(
                response=json.dumps({"message": "You are not teacher"}),
                status=200,
                mimetype="application/json"
            )
        data = request.json

        try:
            req = session.query(Request).get(id)
            if "status" in data:
                if data["status"].lower() == "yes":

                    cours = session.query(Course).get(req.course_id)

                    if cours.students_of_course <= 5:
                        cours.students_of_course += 1
                        req.status = data["status"]
                        studCourse = StudOnCourse(req.student_id, req.course_id)

                        session.add(studCourse)
                        session.add(cours)
                        session.query(Request).filter(Request.id == id).delete()
                        session.flush()
                        session.commit()
                        return Response(
                            response=json.dumps({"message": "Success"}),
                            status=200,
                            mimetype="application/json"
                        )
                    else:
                        session.query(Request).filter(Request.id == id).delete()
                        session.commit()
                        return Response(
                            response=json.dumps({"message": "Course is full"}),
                            status=200,
                            mimetype="application/json"
                        )
                elif data["status"].lower() == "no":
                    session.query(Request).filter(Request.id == id).delete()
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