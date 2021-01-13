import base64
import json
import unittest

from app import app, engine, Base, session, client


class TestUser(unittest.TestCase):
    def setUp(self):
        session.commit()
        Base.metadata.create_all(engine)

    def tearDown(self):
        session.commit()
        Base.metadata.drop_all(bind=engine)

    def test_get_teacher_by_id(self):
        self.assertEqual(client.get('/teach/1', ).status_code, 400)
        self.test_post_teacher()
        self.assertEqual(client.get('/teach/1', ).status_code, 201)

    def test_post_teacher(self):
        error_response = client.post(
            '/teach',
            headers={'Content-Type': 'something',
                     'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(error_response.status_code, 405)

        data = {'firstname': 'first',
                'lastname': 'second',
                'email': 'example18@mail.com',
                'password': 'qwerty'
                }
        encoded_data = json.dumps(data).encode('utf-8')
        response = client.post(
            '/teach',
            data=encoded_data,
            headers={'Content-Type': 'application/json'}
        )
        second_response = client.post(
            '/teach',
            data=encoded_data,
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(second_response.status_code, 401)

    def test_update_teacher(self):
        self.test_post_teacher()
        data = {}
        response = client.put(
            '/teach',
            data=data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 405)
        data = {'firstname': 'first',
                'lastname': 'ahahhah',
                'password': 'qwerty'
                }
        encoded_data = json.dumps(data).encode('utf-8')
        response = client.put(
            '/teach',
            data=encoded_data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 200)

    def test_get_student_by_id(self):
        self.assertEqual(client.get('/stud/1', ).status_code, 400)
        self.test_post_student()
        self.assertEqual(client.get('/stud/1', ).status_code, 201)

    def test_post_student(self):
        with app.test_client() as client:
            error_response = client.post(
                '/stud',
                headers={'Content-Type': 'any',
                         'Authorization': 'Basic ' + base64.b64encode('example20@mail.com:qwerty'.encode()).decode()}
            )
            self.assertEqual(error_response.status_code, 405)

            data = {'firstname': 'first',
                    'lastname': 'second',
                    'email': 'example20@mail.com',
                    'password': 'qwerty'
                    }
            encoded_data = json.dumps(data).encode('utf-8')
            response = client.post(
                '/stud',
                data=encoded_data,
                headers={'Content-Type': 'application/json'}
            )
            second_response = client.post(
                '/stud',
                data=encoded_data,
                headers={'Content-Type': 'application/json'}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(second_response.status_code, 401)

    def test_update_stud(self):
        self.test_post_student()
        data = {}
        response = client.put(
            '/stud',
            data=data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example20@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 405)
        data = {'firstname': 'first',
                'lastname': 'ahahhah',
                'password': 'qwerty'
                }
        encoded_data = json.dumps(data).encode('utf-8')
        response = client.put(
            '/stud',
            data=encoded_data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Basic ' + base64.b64encode('example20@mail.com:qwerty'.encode()).decode()}
        )
        self.assertEqual(response.status_code, 200)
