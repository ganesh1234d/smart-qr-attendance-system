# Pydantic Schemas will be added here later.

from pydantic import BaseModel, EmailStr
from typing import Optional


# ===========================
# USER REGISTER
# ===========================

class UserRegister(BaseModel):
    full_name: str
    batch_no: str
    email: EmailStr
    phone: Optional[str] = None
    department: Optional[str] = None
    password: str


# ===========================
# USER LOGIN
# ===========================

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ===========================
# USER RESPONSE
# ===========================

class UserResponse(BaseModel):
    user_id: int
    email: str
    role: str

    class Config:
        from_attributes = True


# ===========================
# STUDENT RESPONSE
# ===========================

class StudentResponse(BaseModel):
    student_id: int
    full_name: str
    batch_no: str
    phone: str
    department: str

    class Config:
        from_attributes = True


# ===========================
# LOGIN RESPONSE
# ===========================

class LoginResponse(BaseModel):
    access_token: str
    token_type: str


# ===========================
# MARK ATTENDANCE
# ===========================

class AttendanceRequest(BaseModel):
    latitude: float
    longitude: float
    qr_token: str