from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles   # ADD THIS
from fastapi.responses import FileResponse
from app.database import engine, Base
from app.routers import student, admin

from pathlib import Path



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart QR Attendance System",
    description="QR Code + GPS Based Attendance System",
    version="1.0.0"
)


BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")
app.mount("/images", StaticFiles(directory=FRONTEND_DIR / "images"), name="images")




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(student.router)
app.include_router(admin.router)

@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")



@app.get("/health")
def health():
    return {
        "status": "OK",
        "database": "Connected"
    }



@app.get("/login")
def login():
    return FileResponse(FRONTEND_DIR / "login.html")


@app.get("/register")
def register():
    return FileResponse(FRONTEND_DIR / "register.html")


@app.get("/student/attendance-page")
def attendance_page():
    return FileResponse(FRONTEND_DIR / "student" / "attendance.html")


@app.get("/admin/dashboard-page")
def admin_dashboard():
    return FileResponse(FRONTEND_DIR / "admin" / "dashboard.html")



@app.get("/admin/students-page")
def admin_students():
    return FileResponse(FRONTEND_DIR / "admin" / "students.html")


@app.get("/admin/live-attendance-page")
def admin_live_attendance():
    return FileResponse(FRONTEND_DIR / "admin" / "live-attendance.html")


@app.get("/admin/qr-generator-page")
def admin_qr_generator():
    return FileResponse(FRONTEND_DIR / "admin" / "qr_generator.html")


@app.get("/admin/reports-page")
def admin_reports():
    return FileResponse(FRONTEND_DIR / "admin" / "reports.html")