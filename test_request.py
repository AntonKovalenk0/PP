from test_course import *


class TestRequest(unittest.TestCase):
    def setUp(self):
        session.commit()
        Base.metadata.create_all(engine)

    def tearDown(self):
        session.commit()
        Base.metadata.drop_all(bind=engine)

    def test_AddRequest(self):
        data = {'course_id': '1', 'student_id': '2', 'status': 'yes'}
        encoded_data = json.dumps(data).encode('utf-8')
        testCourse = TestCourse()
        testCourse.test_AddCourse()
        response = client.post(
            '/request/1',
            data=encoded_data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 400)
        response = client.post(
            '/request/1',
            data=data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example20@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 405)
        response = client.post(
            '/request/1',
            data=encoded_data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example20@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 200)

    def test_GetRequest(self):
        self.test_AddRequest()
        response = client.get('/request/1', headers={'Content-Type': 'application/json',
                                                     'Authorization': 'Basic ' + base64.b64encode(
                                                         'example20@mail.com:qwerty'.encode()).decode()})
        self.assertEqual(response.status_code, 400)
        response = client.get('/request/123', headers={'Content-Type': 'application/json',
                                                       'Authorization': 'Basic ' + base64.b64encode(
                                                           'example18@mail.com:qwerty'.encode()).decode()})
        self.assertEqual(response.status_code, 404)
        response = client.get('/request/1', headers={'Content-Type': 'application/json',
                                                     'Authorization': 'Basic ' + base64.b64encode(
                                                         'example18@mail.com:qwerty'.encode()).decode()})
        self.assertEqual(response.status_code, 201)

    def test_PutRequest(self):
        data = {'course_id': '1', 'student_id': '2', 'status': 'yes'}
        encoded_data = json.dumps(data).encode('utf-8')
        self.test_AddRequest()
        response = client.put(
            '/request/1',
            data=encoded_data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 400)
        response = client.put(
            '/request/1',
            data=data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example20@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 405)
        response = client.put(
            '/request/1',
            data=encoded_data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example20@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 200)
