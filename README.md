# Student Grades API

REST API for managing students, courses, and academic grades.

## Technologies

- Python 3.13
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Pytest

## Features

- Create, read, update, and delete students
- Create, read, update, and delete courses
- Manage student grades
- Validate input data
- Handle HTTP errors
- Filter students by name
- Paginate student and course lists
- Calculate average grades for students and courses

## Project Structure

```text
grades_api/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── student_grades.sql
├── test_grades_api.py
├── requirements.txt
├── README.md
└── .gitignore
```

The `.env` file must be created locally. It is excluded from Git for security reasons.

## Installation

Clone the repository:

```powershell
git clone https://github.com/stylerok/student-grades-api.git
cd student-grades-api
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Database Configuration

Create a PostgreSQL database named `school`.

Execute the SQL script `student_grades.sql` to create the required tables.

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/school
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

## Run the API

Start the development server:

```powershell
uvicorn main:app --reload
```

API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/students` | Create a student |
| GET | `/students` | List students |
| GET | `/students/{student_id}` | Get a student |
| PATCH | `/students/{student_id}` | Update a student |
| DELETE | `/students/{student_id}` | Delete a student |
| POST | `/courses` | Create a course |
| GET | `/courses` | List courses |
| GET | `/courses/{course_id}` | Get a course |
| PATCH | `/courses/{course_id}` | Update a course |
| DELETE | `/courses/{course_id}` | Delete a course |
| POST | `/grades` | Create a grade |
| GET | `/grades` | List grades |
| GET | `/grades/{grade_id}` | Get a grade |
| PATCH | `/grades/{grade_id}` | Update a grade |
| DELETE | `/grades/{grade_id}` | Delete a grade |
| GET | `/students/{student_id}/grades` | Get student grades |
| GET | `/reports/student-averages` | Student average grades |
| GET | `/reports/course-averages` | Course average grades |

## Run Tests

Run the acceptance tests:

```powershell
pytest -v test_grades_api.py
```

The acceptance test suite verifies API functionality, validation, error handling, database operations, and reports.

**Test result:** 36 passed.