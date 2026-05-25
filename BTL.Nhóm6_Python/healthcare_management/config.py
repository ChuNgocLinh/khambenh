import os
from dotenv import load_dotenv

load_dotenv()

# ================================
# 🗄️ DATABASE CONFIG
# ================================
DB_TYPE = os.getenv("DB_TYPE", "sqlserver")

DB_CONFIG = {
    "DRIVER": "ODBC Driver 17 for SQL Server",
    "SERVER": os.getenv("DB_SERVER", "localhost"),
    "DATABASE": os.getenv("DB_NAME", "HealthcareDB"),
    "USER": os.getenv("DB_USER", "sa"),
    "PASSWORD": os.getenv("DB_PASSWORD", "your_password"),
    "PORT": int(os.getenv("DB_PORT", 3306)),
    "TRUSTED_CONNECTION": "yes",
    "TIMEOUT": 5
}


# ================================
# 🖥️ APP CONFIG
# ================================
APP_CONFIG = {
    "APP_NAME": "Healthcare Management System",
    "VERSION": "1.0",
    "WINDOW_WIDTH": 1200,
    "WINDOW_HEIGHT": 700
}


# ================================
# 🎨 UI CONFIG
# ================================
UI_CONFIG = {
    "PRIMARY_COLOR": "#4CAF50",
    "SECONDARY_COLOR": "#2196F3",
    "BACKGROUND": "#f5f7fb",
    "SIDEBAR_COLOR": "#e8f0fe",
    "HEADER_COLOR": "#ffffff",
    "TEXT_COLOR": "#333333",

    # 👉 đồng bộ font
    "FONT": ("Segoe UI", 10),
    "FONT_BOLD": ("Segoe UI", 12, "bold")
}


# ================================
# 🔐 ROLE CONFIG
# ================================
ROLES = {
    "ADMIN": "admin",
    "DOCTOR": "doctor",
    "STAFF": "staff",
    "PATIENT": "patient"
}


# ================================
# 📊 STATUS CONFIG
# ================================
STATUS = {
    "APPOINTMENT": ["pending", "confirmed", "in_progress", "done", "cancelled"],
    "PAYMENT": ["paid", "unpaid"],
    "MEDICAL": ["in_progress", "completed"]
}


# ================================
# 🔌 CONNECTION STRING
# ================================
def get_connection_string():
    if DB_TYPE == "mysql":
        # Trả về config cho MySQL (sử dụng trong controller)
        return {
            "host": DB_CONFIG["SERVER"],
            "port": DB_CONFIG["PORT"],
            "user": DB_CONFIG["USER"],
            "password": DB_CONFIG["PASSWORD"],
            "database": DB_CONFIG["DATABASE"]
        }
    else:
        # SQL Server connection string
        return (
            f"DRIVER={{{DB_CONFIG['DRIVER']}}};"
            f"SERVER={DB_CONFIG['SERVER']};"
            f"DATABASE={DB_CONFIG['DATABASE']};"
            f"Trusted_Connection={DB_CONFIG['TRUSTED_CONNECTION']};"
            f"Connection Timeout={DB_CONFIG['TIMEOUT']};"
        )


# ================================
# 🧪 DEBUG CONFIG (optional)
# ================================
DEBUG = True

# ================================
# 📅 APPOINTMENT SLOT CONFIG
# ================================
DEFAULT_SLOTS = [
    "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
    "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30",
    "16:00", "16:30", "17:00"
]

DEFAULT_QUEUE_AREA = "3B"
