USE Smart_QR_Attendance_System;
GO

-- ===========================================
-- USERS TABLE
-- ===========================================

CREATE TABLE users
(
    user_id INT IDENTITY(1,1) PRIMARY KEY,

    full_name NVARCHAR(100) NOT NULL,

    email NVARCHAR(150) UNIQUE NOT NULL,

    password_hash NVARCHAR(255) NOT NULL,

    role NVARCHAR(20) NOT NULL
        CHECK(role IN ('Admin','Student')),

    is_active BIT DEFAULT 1,

    created_at DATETIME DEFAULT GETDATE()
);
GO