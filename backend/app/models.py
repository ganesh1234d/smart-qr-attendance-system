from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Float
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


# ===========================
# USERS TABLE
# ===========================
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(200), nullable=False)

    email = Column(String(150), unique=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    role = Column(String(20), default="Student")

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship(
        "Student",
        back_populates="user",
        uselist=False
    )


# ===========================
# STUDENTS TABLE
# ===========================
class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"))

    batch_no = Column(String(30))

    full_name = Column(String(100))

    phone = Column(String(20))

    department = Column(String(100))

    year = Column(String(20))

    section = Column(String(10))

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="student")

    attendance = relationship("Attendance", back_populates="student")

# ===========================
# ATTENDANCE TABLE
# ===========================
class Attendance(Base):
    __tablename__ = "attendance"

    attendance_id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.student_id"))

    attendance_date = Column(DateTime, default=datetime.utcnow)

    status = Column(String(20), default="Present")

    latitude = Column(Float)

    longitude = Column(Float)

    student = relationship("Student", back_populates="attendance")


# ===========================
# QR SESSION TABLE
# ===========================
class QRSession(Base):
    __tablename__ = "qr_sessions"

    session_id = Column(Integer, primary_key=True, index=True)

    qr_token = Column(String(255), unique=True)

    session_date = Column(DateTime)

    start_time = Column(DateTime)

    end_time = Column(DateTime)

    latitude = Column(Float)

    longitude = Column(Float)

    allowed_radius = Column(Float)


# ===========================
# INSTITUTE TABLE
# ===========================
class Institute(Base):
    __tablename__ = "institutes"

    institute_id = Column(Integer, primary_key=True, index=True)

    institute_name = Column(String(200))

    address = Column(String(300))

    latitude = Column(Float)

    longitude = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)