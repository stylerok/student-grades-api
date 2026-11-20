-------------------- Создание таблиц students, courses и grades --------------------

-- 1. Таблица STUDENTS
CREATE TABLE students (
	student_id serial PRIMARY KEY,
	full_name text NOT NULL,
	email text NOT NULL UNIQUE,
	birth_date date,
	enrollment_date date NOT NULL DEFAULT current_date
);

-- 2. Таблица COURSES

CREATE TABLE courses (
	course_id serial PRIMARY KEY,
	course_name text NOT NULL,
	teacher_name text NOT NULL,
	credits integer NOT NULL CHECK (credits > 0)
);

-- 3. Таблица GRADES

CREATE TABLE grades (
	grade_id serial PRIMARY KEY,
	student_id integer NOT NULL REFERENCES students(student_id),
	course_id integer NOT NULL REFERENCES courses(course_id),
	grade numeric(5, 2) NOT NULL CHECK (grade BETWEEN 0 AND 100),
	UNIQUE (student_id, course_id)
);

-------------------- Заполнение данными --------------------

-- 4. Три курса

INSERT INTO courses (
	course_name, 
	teacher_name, 
	credits
)
VALUES
	('Databases', 'Jordan Ball', 5),
	('Statistics', 'Mia Howard', 4),
	('Algorithms', 'Oscar Shaw', 6);

-- 5. Три студента

INSERT INTO students (
	full_name, 
	email, 
	birth_date
)
VALUES
	('Andrew Johnson', 'andrew@example.com', '2003-05-11'),
	('Maria Brown', 'maria@example.com', NULL),
	('Arthur Matthews', 'arthur@example.com', NULL);

-- 6. Четыре оценки

INSERT INTO grades (
	student_id, 
	course_id, 
	grade
)
SELECT 
	s.student_id, 	
	c.course_id, 
	v.grade
FROM (
	VALUES
		('andrew@example.com', 'Databases', 95.00),
		('andrew@example.com', 'Statistics', 88.50),
		('maria@example.com', 'Databases', 76.00),
		('maria@example.com', 'Algorithms', 91.00)
) AS v(email, course_name, grade)
JOIN students s ON s.email = v.email
JOIN courses c ON c.course_name = v.course_name;

-------------------- Обновление --------------------

-- 7. Заполняем birth_date

UPDATE students
SET birth_date = '2004-08-02'
WHERE email = 'maria@example.com';

-- 8. Исправляем email

UPDATE students
SET email = 'andrew.johnson@example.com'
WHERE email = 'andrew@example.com';

-------------------- Удаление --------------------

-- 9. Удаляем студента без оценок

DELETE FROM students
WHERE email = 'arthur@example.com';

-------------------- Проверка результата --------------------

SELECT * FROM students;
SELECT * FROM courses;

SELECT
	s.full_name,
	c.course_name,
	g.grade
FROM grades g
JOIN students s ON g.student_id = s.student_id
JOIN courses c ON g.course_id = c.course_id;