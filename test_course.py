from test_user import *
import json


class TestCourse(unittest.TestCase):
    def setUp(self):
        session.commit()
        Base.metadata.create_all(engine)

    def tearDown(self):
        session.commit()
        Base.metadata.drop_all(bind=engine)

    def test_AddCourse(self):
        testUser = TestUser()
        testUser.test_post_teacher()
        data = {'name': 'Math'}
        baddata = {'nfdadae': 'Mdh'}
        encoded_data = json.dumps(data).encode('utf-8')
        encoded_baddata = json.dumps(baddata).encode('utf-8')
        response = client.post(
            '/course',
            data=encoded_data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwertyyy'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 401)
        response = client.post(
            '/course',
            data=encoded_baddata,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 405)
        response = client.post(
            '/course',
            data=encoded_data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 200)
        testUser.test_post_student()

        error_response = client.post(
            '/course',
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example20@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(error_response.status_code, 400)

    def test_UpdateCourse(self):
        self.test_AddCourse()
        data = {'name': 'English', 'owner_id': '1', 'students_of_course': '5'}
        encoded_data = json.dumps(data).encode('utf-8')
        response = client.put(
            '/course/1',
            data=encoded_data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example20@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 400)
        response = client.put(
            '/course/1',
            data=data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 405)
        response = client.put(
            '/course/1',
            data=encoded_data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 200)

        error_response = client.put(
            '/course/1',
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example20@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(error_response.status_code, 400)

    def test_GetCourse(self):
        self.assertEqual(client.get('course/21').status_code, 404)
        self.test_AddCourse()
        self.assertEqual(client.get('course/1').status_code, 201)

    def test_DeleteCourse(self):
        testUser = TestUser()
        testUser.test_post_teacher()
        response = client.put(
            '/course',
            headers={'Content-Type': 'any',
                     'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 405)
        testUser.test_post_student()
        response = client.put(
            '/course',
            headers={'Content-Type': 'any',
                     'Authorization': 'Basic ' + base64.b64encode('example20@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 405)

    def test_GetAllCourses(self):
        self.assertEqual(client.get('/allcourses').status_code, 404)
        self.test_AddCourse()
        self.assertEqual(client.get('/allcourses').status_code, 201)


