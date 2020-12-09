CREATE TABLE teachers (
    id INT NOT NULL,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE students (
    id INT NOT NULL,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE courses (
    id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    owner_id INT NOT NULL,
    FOREIGN KEY(owner_id) REFERENCES teachers(id),
    students_of_course INT CHECK (status between 0 and 5) NOT NULL,
    status INT CHECK (status between 0 and 2) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE requests (
    id INT NOT NULL,
    course_id INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    student_id INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    PRIMARY KEY (id)
);

CREATE TABLE users (
    id INT NOT NULL,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    status INT CHECK (status between 0 and 2) NOT NULL,
    PRIMARY KEY (id)
);


