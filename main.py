from fastapi import FastAPI, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from database import get_db
from models import Student, Course, Grade
from schemas import (
    StudentCreate,
    StudentUpdate,
    StudentOut,
    CourseCreate,
    CourseUpdate,
    CourseOut,
    GradeCreate,
    GradeUpdate,
    GradeOut,
    StudentAverageOut,
    CourseAverageOut,
)

app = FastAPI(title="Student Grades API")


# =========================
# STUDENTS
# =========================

@app.post(
    "/students",
    response_model=StudentOut,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    payload: StudentCreate,
    db: Session = Depends(get_db),
):
    student = Student(**payload.model_dump())

    db.add(student)

    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Student with this email already exists",
        )

    return student


@app.get("/students", response_model=list[StudentOut])
def list_students(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    name: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Student)

    if name:
        query = query.filter(Student.full_name.ilike(f"%{name}%"))

    return (
        query
        .order_by(Student.student_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@app.get("/students/{student_id}", response_model=StudentOut)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    student = db.get(Student, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return student


@app.patch("/students/{student_id}", response_model=StudentOut)
def update_student(
    student_id: int,
    payload: StudentUpdate,
    db: Session = Depends(get_db),
):
    student = db.get(Student, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(student, field, value)

    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Student with this email already exists",
        )

    return student


@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    student = db.get(Student, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    db.query(Grade).filter(
        Grade.student_id == student_id
    ).delete()

    db.delete(student)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# =========================
# COURSES
# =========================

@app.post(
    "/courses",
    response_model=CourseOut,
    status_code=status.HTTP_201_CREATED,
)
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db),
):
    course = Course(**payload.model_dump())

    db.add(course)
    db.commit()
    db.refresh(course)

    return course


@app.get("/courses", response_model=list[CourseOut])
def list_courses(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return (
        db.query(Course)
        .order_by(Course.course_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@app.get("/courses/{course_id}", response_model=CourseOut)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
):
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    return course


@app.patch("/courses/{course_id}", response_model=CourseOut)
def update_course(
    course_id: int,
    payload: CourseUpdate,
    db: Session = Depends(get_db),
):
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(course, field, value)

    db.commit()
    db.refresh(course)

    return course


@app.delete(
    "/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
):
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    has_grades = (
        db.query(Grade)
        .filter(Grade.course_id == course_id)
        .first()
    )

    if has_grades:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a course that has grades",
        )

    db.delete(course)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# =========================
# GRADES
# =========================

@app.post(
    "/grades",
    response_model=GradeOut,
    status_code=status.HTTP_201_CREATED,
)
def create_grade(
    payload: GradeCreate,
    db: Session = Depends(get_db),
):
    student = db.get(Student, payload.student_id)

    if student is None:
        raise HTTPException(
            status_code=400,
            detail="Student not found",
        )

    course = db.get(Course, payload.course_id)

    if course is None:
        raise HTTPException(
            status_code=400,
            detail="Course not found",
        )

    existing_grade = (
        db.query(Grade)
        .filter(
            Grade.student_id == payload.student_id,
            Grade.course_id == payload.course_id,
        )
        .first()
    )

    if existing_grade:
        raise HTTPException(
            status_code=409,
            detail="Grade already exists for this student and course",
        )

    grade = Grade(**payload.model_dump())

    db.add(grade)

    try:
        db.commit()
        db.refresh(grade)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Grade already exists for this student and course",
        )

    return grade


@app.get("/grades", response_model=list[GradeOut])
def list_grades(
    student_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Grade)

    if student_id is not None:
        student = db.get(Student, student_id)

        if student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found",
            )

        query = query.filter(Grade.student_id == student_id)

    return query.order_by(Grade.grade_id).all()


@app.get(
    "/students/{student_id}/grades",
    response_model=list[GradeOut],
)
def list_student_grades(
    student_id: int,
    db: Session = Depends(get_db),
):
    student = db.get(Student, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return (
        db.query(Grade)
        .filter(Grade.student_id == student_id)
        .order_by(Grade.grade_id)
        .all()
    )


@app.get("/grades/{grade_id}", response_model=GradeOut)
def get_grade(
    grade_id: int,
    db: Session = Depends(get_db),
):
    grade = db.get(Grade, grade_id)

    if grade is None:
        raise HTTPException(
            status_code=404,
            detail="Grade not found",
        )

    return grade


@app.patch("/grades/{grade_id}", response_model=GradeOut)
def update_grade(
    grade_id: int,
    payload: GradeUpdate,
    db: Session = Depends(get_db),
):
    grade = db.get(Grade, grade_id)

    if grade is None:
        raise HTTPException(
            status_code=404,
            detail="Grade not found",
        )

    grade.grade = payload.grade

    db.commit()
    db.refresh(grade)

    return grade


@app.delete(
    "/grades/{grade_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_grade(
    grade_id: int,
    db: Session = Depends(get_db),
):
    grade = db.get(Grade, grade_id)

    if grade is None:
        raise HTTPException(
            status_code=404,
            detail="Grade not found",
        )

    db.delete(grade)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# =========================
# REPORTS
# =========================

@app.get(
    "/reports/student-averages",
    response_model=list[StudentAverageOut],
)
def student_averages(
    db: Session = Depends(get_db),
):
    results = (
        db.query(
            Student.student_id,
            Student.full_name,
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
            func.count(Grade.grade).label("courses_taken"),
        )
        .join(Grade, Grade.student_id == Student.student_id)
        .group_by(Student.student_id, Student.full_name)
        .order_by(Student.student_id)
        .all()
    )

    return [
        {
            "student_id": row.student_id,
            "full_name": row.full_name,
            "average_grade": float(row.average_grade),
            "courses_taken": row.courses_taken,
        }
        for row in results
    ]


@app.get(
    "/reports/course-averages",
    response_model=list[CourseAverageOut],
)
def course_averages(
    db: Session = Depends(get_db),
):
    results = (
        db.query(
            Course.course_id,
            Course.course_name,
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
            func.count(Grade.grade).label("students_graded"),
        )
        .join(Grade, Grade.course_id == Course.course_id)
        .group_by(Course.course_id, Course.course_name)
        .order_by(Course.course_id)
        .all()
    )

    return [
        {
            "course_id": row.course_id,
            "course_name": row.course_name,
            "average_grade": float(row.average_grade),
            "students_graded": row.students_graded,
        }
        for row in results
    ]
