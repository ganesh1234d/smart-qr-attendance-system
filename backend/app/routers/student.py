from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, Date
import math
from app.models import QRSession
from app.database import get_db
from app.models import User, Student
from app.schemas import UserRegister, UserLogin
from app.models import Attendance
from app.schemas import AttendanceRequest
from datetime import datetime, date
from app.auth import (
    hash_password,
    verify_password,
    create_access_token     
)

router = APIRouter(
    prefix="/student",
    tags=["Student"]
)


# ==========================================
# REGISTER
# ==========================================

@router.post("/register")
def register_student(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    # Check Email
    existing_email = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

 

    # Encrypt Password
    encrypted_password = hash_password(
        user.password
    )

    # Save User
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password_hash=encrypted_password,
        role="Student"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Save Student
    new_student = Student(
        user_id=new_user.user_id,
        full_name=user.full_name,
        batch_no=user.batch_no,
    

    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Registration Successful",
        "student_id": new_student.student_id
    }


# ==========================================
# LOGIN
# ==========================================

@router.post("/login")
def login_student(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Email"
        )

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Password"
        )

    token = create_access_token(
        {
            "user_id": db_user.user_id,
            "email": db_user.email,
            "role": db_user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user.role,
        "message": "Login Successful"
    }


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from app.auth import verify_token

# ==========================================
# JWT Security
# ==========================================

security = HTTPBearer()


# ==========================================
# Get Current User
# ==========================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token"
        )

    user = (
        db.query(User)
        .filter(User.user_id == payload["user_id"])
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# ==========================================
# STUDENT PROFILE
# ==========================================

@router.get("/profile")
def student_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    student = (
        db.query(Student)
        .filter(Student.user_id == current_user.user_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found."
        )

    return {

        "student_id": student.student_id,

        "name": student.full_name,

        "email": current_user.email,

        "batch_no": student.batch_no,

  



    }


# ==========================================
# DASHBOARD
# ==========================================

@router.get("/dashboard")
def dashboard(
    current_user: User = Depends(get_current_user)
):

    return {

        "message": "Welcome to Smart QR Attendance",

        "user": current_user.email,

        "role": current_user.role
    }


# ==========================================
# TOKEN CHECK
# ==========================================

@router.get("/verify-token")
def verify_login(
    current_user: User = Depends(get_current_user)
):

    return {

        "status": "success",

        "message": "Token is valid.",

        "email": current_user.email
    }


# ==========================================
# MARK ATTENDANCE
# ==========================================

@router.post("/mark-attendance")
def mark_attendance(
    attendance: AttendanceRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    student = (
        db.query(Student)
        .filter(Student.user_id == current_user.user_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    # Validate QR session token
    today = date.today()

    qr_session = (
        db.query(QRSession)
        .filter(QRSession.qr_token == attendance.qr_token)
        .first()
    )

    if not qr_session:
        raise HTTPException(
            status_code=400,
            detail="Invalid QR Code."
        )

    if qr_session.session_date.date() != today:
        raise HTTPException(
            status_code=400,
            detail="This QR Code has expired. Please scan today's QR Code."
        )

    # ==========================================
    # VALIDATE GPS DISTANCE (Haversine formula)
    # ==========================================

    def calculate_distance(lat1, lon1, lat2, lon2):

        R = 6371000  # Earth radius in meters

        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)

        a = (
            math.sin(d_lat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(d_lon / 2) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    distance = calculate_distance(
        attendance.latitude,
        attendance.longitude,
        qr_session.latitude,
        qr_session.longitude
    )

    if distance > qr_session.allowed_radius:
        raise HTTPException(
            status_code=400,
            detail=f"You must be within the institute campus to mark attendance. You are {int(distance)}m away."
        )

    # Check today's attendance
    existing = (
        db.query(Attendance)
        .filter(
            Attendance.student_id == student.student_id
        )
        .all()
    )

    for record in existing:
        if record.attendance_date.date() == today:
            raise HTTPException(
                status_code=400,
                detail="Attendance already marked today."
            )

    new_attendance = Attendance(

        student_id=student.student_id,

        attendance_date=datetime.utcnow(),

        status="Present",

        latitude=attendance.latitude,

        longitude=attendance.longitude

    )

    db.add(new_attendance)

    db.commit()

    return {

        "message": "Attendance Marked Successfully"

    }

# ==========================================
# ADMIN - TOTAL STUDENTS
# ==========================================

@router.get("/admin/total-students")
def total_students(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
        )

    total = db.query(Student).count()

    return {
        "total_students": total
    }# ==========================================
# ADMIN - TODAY ATTENDANCE
# ==========================================



@router.get("/admin/today-attendance")
def today_attendance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
        )

    today = date.today()

    present = db.query(Attendance).filter(
        func.cast(
            Attendance.attendance_date,
            Date
        ) == today
    ).count()

    return {
        "present": present
    }



# ==========================================
# ADMIN - ABSENT COUNT
# ==========================================

@router.get("/admin/absent-count")
def absent_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
        )

    total = db.query(Student).count()

    today = date.today()

    present = db.query(Attendance).filter(
        func.cast(
            Attendance.attendance_date,
            Date
        ) == today
    ).count()

    return {
        "absent": total - present
    }


# ==========================================
# ADMIN - STUDENT LIST
# ==========================================

@router.get("/admin/students")
def all_students(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
        )

    students = db.query(Student).all()

    result = []

    for s in students:

        result.append({

            "student_id": s.student_id,

            "name": s.full_name,

            "batch_no": s.batch_no,

            "email": s.user.email


        })

    return result