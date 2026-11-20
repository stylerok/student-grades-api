from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Student(Base):
    __tablename__ = "students"
    student_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    enrollment_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        server_default=func.current_date(),
    )


class Course(Base):
    __tablename__ = "courses"
    course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_name: Mapped[str] = mapped_column(Text, nullable=False)
    instructor_name: Mapped[str] = mapped_column(
        "teacher_name",
        Text,
        nullable=False,
    )
    credits: Mapped[int] = mapped_column(Integer, nullable=False)


class Grade(Base):
    __tablename__ = "grades"
    grade_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.student_id"),
        nullable=False,
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.course_id"),
        nullable=False,
    )

    grade: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )