from database import get_db_connection
from database import DB_PATH

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

print("Creating database at:", DB_PATH)

conn = get_db_connection()

conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL,
    department TEXT NOT NULL
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS announcements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    date TEXT NOT NULL
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS shifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    department TEXT NOT NULL,
    location TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    content TEXT NOT NULL
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    location TEXT NOT NULL,
    level TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Đã tiếp nhận'
)
""")

employee_password_hash = pwd_context.hash("admin123")
admin_password_hash = pwd_context.hash("admin123")

conn.execute("""
INSERT OR IGNORE INTO users (
    id, username, password, full_name, role, department
)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    1,
    "admin",
    employee_password_hash,
    "Nguyễn Văn An",
    "employee",
    "An ninh"
))

conn.execute("""
INSERT OR IGNORE INTO users (
    id, username, password, full_name, role, department
)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    2,
    "superadmin",
    admin_password_hash,
    "Quản trị hệ thống",
    "admin",
    "IT"
))

conn.execute("""
INSERT OR IGNORE INTO announcements (id, title, content, date)
VALUES
(
    1,
    'Thông báo kiểm tra an ninh',
    'Tất cả nhân viên cần tuân thủ quy trình kiểm tra thẻ ra vào khu vực hạn chế.',
    '04/05/2026'
),
(
    2,
    'Lịch đào tạo nội bộ',
    'Buổi đào tạo quy trình xử lý hành lý sẽ diễn ra vào thứ Hai tuần tới.',
    '05/05/2026'
),
(
    3,
    'Cập nhật quy trình khai thác',
    'Nhân viên bộ phận khai thác cần đọc tài liệu quy trình mới trước ca làm việc.',
    '06/05/2026'
)
""")

conn.execute("""
INSERT OR IGNORE INTO shifts (id, date, time, department, location, status)
VALUES
(
    1,
    '04/05/2026',
    '06:00 - 14:00',
    'An ninh',
    'Cổng kiểm soát A',
    'Sắp tới'
),
(
    2,
    '05/05/2026',
    '14:00 - 22:00',
    'Mặt đất',
    'Khu vực check-in',
    'Sắp tới'
),
(
    3,
    '06/05/2026',
    '22:00 - 06:00',
    'Khai thác',
    'Phòng điều phối',
    'Sắp tới'
)
""")

conn.execute("""
INSERT OR IGNORE INTO documents (id, title, category, content)
VALUES
(
    1,
    'Quy trình kiểm tra thẻ nhân viên',
    'An ninh',
    'Nhân viên phải xuất trình thẻ khi vào khu vực hạn chế. Không cho mượn thẻ dưới mọi hình thức.'
),
(
    2,
    'Quy trình xử lý hành lý thất lạc',
    'Dịch vụ hành khách',
    'Khi nhận thông tin hành lý thất lạc, nhân viên cần lập biên bản, kiểm tra mã hành lý và liên hệ bộ phận liên quan.'
),
(
    3,
    'Quy trình báo cáo sự cố',
    'Khai thác',
    'Mọi sự cố trong quá trình khai thác phải được báo cáo ngay cho trưởng ca và ghi nhận vào hệ thống.'
)
""")

conn.commit()
conn.close()

print("Database created successfully.")