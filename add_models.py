from models import Session, Teacher, Student, Request, User, Course

session1 = Session()

Teacher1 = Teacher(id=1, firstname='Misha', lastname='Chex', password='1wr32')
Teacher2 = Teacher(id=2, firstname='Inessa', lastname='Pomirko', password='fsod2')

Student1 = Student(id=1, firstname='Nazar', lastname='Kalapun', password='121e2')
Student2 = Student(id=2, firstname='Anton', lastname='Koval', password='dasas')

Course1 = Course(id=1, name='PP', owner_id=1, students_of_course=2, status=1)

Request1 = Request(id=1, course_id=1, student_id=1)
# Request2 = Request(id=2, courseId='2', studentId=2)

User1 = User(id=1, firstname='Misha', lastname="Chex", email="mehachex@gmail.com", phone="0678278198", status=1)


session1.add(Teacher1)
session1.commit()
session1.add(Teacher2)
session1.commit()

session1.add(Student1)
session1.commit()
session1.add(Student2)
session1.commit()


session1.add(Course1)
session1.commit()

session1.add(Request1)
session1.commit()

session1.add(User1)
session1.commit()

session1.close()

