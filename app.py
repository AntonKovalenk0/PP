from flask import Flask, json, Response, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker

from models import *

app = Flask(__name__)
api = Api(app)

engine = create_engine('postgresql://postgres:1234@localhost/mydb', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

client = app.test_client()


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


auth = HTTPBasicAuth()


@auth.verify_password
def verify_passsword(username, password):
    # session = Session()
    user = session.query(User).filter_by(email=username).first()
    if user:
        if check_password_hash(user.password, password):
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

        if user.status != 'teacher':
            return Response(
                response=json.dumps({"message": "You are not teacher"}),
                status=400,
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
        if user.status != 'teacher':
            return Response(
                response=json.dumps({"message": "You are not teacher"}),
                status=400,
                mimetype="application/json"
            )
        try:
            data = request.json
            course1 = session.query(Course).get(cid)
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
            teacher = User(data["firstname"], data["lastname"], data["email"], data["password"], "teacher")
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
                    response=json.dumps({"message": "Email already exist"}),
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
                student = User(data["firstname"], data["lastname"], data["email"], data["password"], "student")
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
    def put(self):
        user = auth.current_user()
        try:
            data = request.json
            user = session.query(User).get(user.id)
            if "firstname" in data:
                user.firstname = data["firstname"]
            if "lastname" in data:
                user.lastname = data["lastname"]
            if "password" in data:
                user.password = data["password"]
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
    def put(self):
        user = auth.current_user()
        try:
            data = request.json
            user = session.query(User).get(user.id)
            if "firstname" in data:
                user.firstname = data["firstname"]
            if "lastname" in data:
                user.lastname = data["lastname"]
            if "password" in data:
                user.password = generate_password_hash(data['password'])
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


class AddRequest(Resource):
    @auth.login_required
    def post(self, cid):
        user = auth.current_user()
        if user.status != 'student':
            return Response(
                response=json.dumps({"message": "You are not student"}),
                status=400,
                mimetype="application/json"
            )
        try:
            data = request.json
            req = Request(course_id=cid, student_id=0, status='yes')
            if "student_id" in data:
                req.student_id = data["student_id"]
            if "status" in data:
                req.status = data["status"]
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
        if user.status != 'teacher':
            return Response(
                response=json.dumps({"message": "You are not teacher"}),
                status=400,
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
    def put(self, rid):
        user = auth.current_user()
        if user.status != 'student':
            return Response(
                response=json.dumps({"message": "You are not student"}),
                status=400,
                mimetype="application/json"
            )
        try:
            data = request.json
            req = session.query(Request).get(rid)
            if "course_id" in data:
                req.course_id = data["course_id"]
            if "student_id" in data:
                req.student_id = data["student_id"]
            if "status" in data:
                req.status = data["status"]
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


api.add_resource(AddCourse, '/course')
api.add_resource(UpdateCourse, '/course/<int:cid>')
api.add_resource(GetCourse, '/course/<int:id>')

api.add_resource(Addteacher, '/teach')
api.add_resource(AddStudent, '/stud')
api.add_resource(UpdateTeacher, '/teach')
api.add_resource(UpdateStudent, '/stud')
api.add_resource(GetTeacher, '/teach/<int:id>')
api.add_resource(GetStudent, '/stud/<int:id>')
api.add_resource(GetAllCourses, '/allcourses')

api.add_resource(AddRequest, '/request/<int:cid>')
api.add_resource(GetRequest, '/request/<int:id>')
api.add_resource(UpdateReq, '/request/<int:rid>')

if __name__ == "__main__":
    # test_app.foo()
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
