from openpyxl import Workbook
from fastapi.responses import FileResponse
import os

import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, date ,time

from app.models import QRSession


from app.database import get_db
from app.models import User, Student, Attendance
from app.routers.student import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# ===============================
# Total Students
# ===============================
@router.get("/total-students")
def total_students(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
        )

    return {
        "total_students": db.query(Student).count()
    }


# ===============================
# Today's Attendance
# ===============================
@router.get("/today-attendance")
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

    count = 0

    attendance = db.query(Attendance).all()

    for record in attendance:

        if record.attendance_date.date() == today:

            count += 1

    return {
        "today_attendance": count
    }


# ===============================
# Absent Students
# ===============================
@router.get("/absent-count")
def absent_students(
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

    present = 0

    attendance = db.query(Attendance).all()

    for record in attendance:

        if record.attendance_date.date() == today:

            present += 1

    return {
        "absent": total - present
    }


# ===============================
# Student List
# ===============================
@router.get("/students")
def get_students(
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

            "full_name": s.full_name,

            "batch_no": s.batch_no,

            "email": s.user.email

        })

    return result


# ===============================
# LIVE ATTENDANCE
# ===============================
@router.get("/live-attendance")
def live_attendance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
        )

    today = date.today()

    records = db.query(Attendance).all()

    result = []

    for record in records:

        if record.attendance_date.date() == today:

            student = db.query(Student).filter(
                Student.student_id == record.student_id
            ).first()

            result.append({

                "student_id": student.student_id,

                "name": student.full_name,

                "batch_no": student.batch_no,

                "department": student.department,

                "time": record.attendance_date.strftime("%I:%M:%S %p"),

                "latitude": record.latitude,

                "longitude": record.longitude,

                "status": record.status

            })

    return result



# ===============================
# DATE-WISE REPORT
# ===============================
@router.get("/report")
def attendance_report(
    report_date: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
        )

    # If no date is selected, use today's date
    if report_date:

        selected_date = datetime.strptime(
            report_date,
            "%Y-%m-%d"
        ).date()

    else:

        selected_date = date.today()

    students = db.query(Student).all()

    attendance = db.query(Attendance).all()

    report = []

    present_count = 0

    for student in students:

        status = "Absent"

        time = "-"

        for record in attendance:

            if (
                record.student_id == student.student_id
                and record.attendance_date.date() == selected_date
            ):

                status = "Present"

                time = record.attendance_date.strftime("%I:%M %p")

                present_count += 1

                break

        report.append({

            "student_id": student.student_id,

            "batch_no": student.batch_no,

            "name": student.full_name,

            "department": student.department,

            "time": time,

            "status": status

        })

    total = len(students)

    absent = total - present_count

    percentage = 0

    if total > 0:

        percentage = round(
            (present_count / total) * 100,
            2
        )

    return {

        "date": str(selected_date),

        "total_students": total,

        "present": present_count,

        "absent": absent,

        "attendance_percentage": percentage,

        "students": report

    }




# ======================================
# EXPORT ATTENDANCE REPORT TO EXCEL
# ======================================

@router.get("/export-excel")
def export_excel(
    report_date: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Admin only
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
        )

    # Selected date
    if report_date:

        selected_date = datetime.strptime(
            report_date,
            "%Y-%m-%d"
        ).date()

    else:

        selected_date = date.today()

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Attendance Report"

    # Header Row
    sheet.append([
        "Student ID",
        "Name",
        "Batch No",
        "Department",
        "Time",
        "Status"
    ])

    students = db.query(Student).all()

    attendance = db.query(Attendance).all()

    for student in students:

        status = "Absent"
        time = "-"

        for record in attendance:

            if (
                record.student_id == student.student_id
                and record.attendance_date.date() == selected_date
            ):

                status = "Present"

                time = record.attendance_date.strftime("%I:%M %p")

                break

        sheet.append([

            student.student_id,

            student.full_name,

            student.batch_no,

            student.department,

            time,

            status

        ])

    filename = "Attendance_Report.xlsx"

    workbook.save(filename)

    return FileResponse(

        path=filename,

        filename=filename,

        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )




# ===============================
# GENERATE TODAY'S QR SESSION
# ===============================
@router.post("/generate-qr-session")
def generate_qr_session(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
        )

    today = date.today()

    new_token = uuid.uuid4().hex

    new_session = QRSession(
        qr_token=new_token,
        session_date=datetime.combine(today, time.min),
        start_time=datetime.utcnow(),
        end_time=datetime.combine(today, time.max),
        latitude=17.482959817777086,
        longitude=78.39431604254752,
        allowed_radius=50
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return {
        "session_id": new_token,
        "valid_date": str(today)
    }