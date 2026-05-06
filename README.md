# Airport Internal App

README này gom toàn bộ các bước đã làm từ đầu đến hiện tại cho hệ thống:

- Mobile App Flutter
- Backend API FastAPI
- Database SQLite
- Chạy app trên điện thoại Android thật
- Kết nối Mobile App với Backend
- Lưu dữ liệu vào SQLite
- Chatbot nội bộ đơn giản
- Báo cáo sự cố và danh sách sự cố

---

# 1. Mục tiêu hệ thống

Mục tiêu ban đầu:

```text
Mobile App + Admin Web + Backend API + Database
```

Trong giai đoạn hiện tại, ta đã làm phần:

```text
Mobile App Flutter
        ↓
Backend API FastAPI
        ↓
SQLite Database
```

Admin Web sẽ làm sau.

---

# 2. Kiến trúc hiện tại

```text
Flutter Mobile App
        ↓ gọi HTTP API
FastAPI Backend API
        ↓ đọc/ghi
SQLite Database
```

Mobile App không truy cập database trực tiếp. Tất cả dữ liệu đi qua Backend API.

---

# 3. Thư mục project

Hiện tại có 2 thư mục chính:

```text
C:\Users\PC\airport_mobile_app
C:\Users\PC\airport_backend
```

Nên mở cả 2 thư mục trong cùng một VS Code Workspace.

---

# 4. Cấu trúc Mobile App

```text
airport_mobile_app/
├── lib/
│   ├── main.dart
│   ├── config/
│   │   └── api_config.dart
│   └── screens/
│       ├── login_screen.dart
│       ├── dashboard_screen.dart
│       ├── announcements_screen.dart
│       ├── shifts_screen.dart
│       ├── documents_screen.dart
│       ├── profile_screen.dart
│       ├── incidents_screen.dart
│       ├── incident_report_screen.dart
│       └── chatbot_screen.dart
│
├── pubspec.yaml
└── android/
```

---

# 5. Cấu trúc Backend

```text
airport_backend/
├── main.py
├── database.py
├── init_db.py
├── airport.db
├── requirements.txt
└── venv/
```

---

# 6. Công nghệ sử dụng

## Mobile App

- Flutter
- Dart
- Package `http`
- Chạy trên điện thoại Android thật qua USB

## Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLite

## Database

- SQLite
- File database: `airport.db`

---

# 7. Tài khoản demo

```text
Username: admin
Password: admin123
```

Tài khoản này hiện được lưu trong bảng `users`.

---

# 8. Các bước đã làm

## Bước 1: Kiểm tra Flutter

Chạy:

```powershell
flutter doctor
```

Kết quả cần đạt:

```text
Flutter: OK
Android toolchain: OK
Connected device: OK
```

Lỗi Visual Studio cho Windows app có thể bỏ qua nếu chỉ làm Android.

---

## Bước 2: Kiểm tra điện thoại Android

Chạy:

```powershell
flutter devices
```

Thiết bị đã nhận:

```text
SM S711B • R5CX40LFFQD • android-arm64
```

---

## Bước 3: Tạo Flutter project

```powershell
flutter create airport_mobile_app
cd airport_mobile_app
code .
```

---

## Bước 4: Chạy app mẫu lên điện thoại

```powershell
flutter run -d R5CX40LFFQD
```

---

## Bước 5: Tạo màn hình đăng nhập

File:

```text
lib/main.dart
```

Đã tạo màn hình:

- Logo sân bay
- Tên app
- Ô username
- Ô password
- Nút đăng nhập
- Tài khoản demo `admin/admin123`

---

## Bước 6: Tạo Dashboard

Sau khi đăng nhập đúng, app chuyển sang Dashboard.

Dashboard có 6 ô:

```text
Thông báo
Ca trực
Tài liệu
Chatbot
Sự cố
Cá nhân
```

Đã sửa lỗi overflow bằng:

```dart
childAspectRatio: 0.95
```

và giảm size icon/text.

---

## Bước 7: Tạo màn hình Thông báo

Đã tạo `AnnouncementsScreen`.

Ban đầu dữ liệu là danh sách mẫu trong Flutter.

---

## Bước 8: Làm giao diện Thông báo gọn hơn

Đã thay `ListTile` bằng card custom gồm:

- Icon
- Tiêu đề
- Nội dung
- Ngày

---

## Bước 9: Tạo màn hình Ca trực

Đã tạo `ShiftsScreen`.

Ban đầu dữ liệu là danh sách mẫu trong Flutter.

---

## Bước 10: Tạo màn hình Tài liệu

Đã tạo `DocumentsScreen`.

Ban đầu dữ liệu là danh sách mẫu trong Flutter.

---

## Bước 11: Tạo màn hình Chatbot đơn giản

Đã tạo `ChatbotScreen`.

Ban đầu chatbot trả lời mẫu trong app.

---

## Bước 12: Tạo màn hình Báo cáo sự cố

Đã tạo `IncidentReportScreen`.

Form gồm:

```text
Tiêu đề sự cố
Vị trí xảy ra
Mức độ
Mô tả chi tiết
Nút gửi báo cáo
```

---

## Bước 13: Tạo màn hình Cá nhân

Đã tạo `ProfileScreen`.

Hiển thị:

```text
Họ tên
Mã nhân viên
Phòng ban
Chức vụ
Số điện thoại
Email
```

---

## Bước 14: Chỉnh cỡ chữ toàn app

Trong `main.dart`, đã dùng:

```dart
builder: (context, child) {
  return MediaQuery(
    data: MediaQuery.of(context).copyWith(
      textScaler: const TextScaler.linear(0.9),
    ),
    child: child!,
  );
},
```

Mục đích: tránh chữ quá to trên điện thoại.

---

## Bước 15: Bật lại màn hình đăng nhập

Trong `main.dart`:

```dart
home: const LoginScreen(),
```

---

## Bước 16: Tách code Flutter thành nhiều file

Đã tạo thư mục:

```text
lib/screens
```

và tách các màn hình:

```text
login_screen.dart
dashboard_screen.dart
announcements_screen.dart
shifts_screen.dart
documents_screen.dart
chatbot_screen.dart
incident_report_screen.dart
profile_screen.dart
incidents_screen.dart
```

`main.dart` chỉ còn app root và theme.

---

## Bước 17: Tạo Backend FastAPI

Tạo thư mục:

```text
C:\Users\PC\airport_backend
```

Tạo môi trường ảo:

```powershell
python -m venv venv
venv\Scripts\activate
```

Cài thư viện:

```powershell
pip install fastapi uvicorn
```

Tạo `main.py` ban đầu:

```python
from fastapi import FastAPI

app = FastAPI(title="Airport Internal Backend API")


@app.get("/")
def home():
    return {
        "message": "Airport Backend API is running"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "ok"
    }
```

Chạy:

```powershell
uvicorn main:app --reload
```

Mở:

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
```

---

## Bước 18: Cho điện thoại truy cập Backend

Dừng backend rồi chạy lại:

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Lấy IP máy tính:

```powershell
ipconfig
```

IP hiện tại:

```text
192.168.10.190
```

Trên điện thoại mở:

```text
http://192.168.10.190:8000
```

---

## Bước 19: Tạo API đăng nhập

Thêm model:

```python
class LoginRequest(BaseModel):
    username: str
    password: str
```

API ban đầu kiểm tra `admin/admin123` trong code. Sau này đã đổi sang kiểm tra từ SQLite.

---

## Bước 20: Cài package HTTP cho Flutter

Trong project Flutter:

```powershell
flutter pub add http
flutter pub get
```

---

## Bước 21: Flutter gọi API đăng nhập

Trong `login_screen.dart`:

- Thêm `dart:convert`
- Thêm package `http`
- Gửi POST đến `/api/auth/login`
- Sau khi đăng nhập thành công thì mở Dashboard

---

## Bước 22: Tạo API Thông báo

Backend API:

```text
GET /api/announcements
```

Ban đầu trả dữ liệu cứng. Sau này đã đổi sang lấy từ SQLite.

---

## Bước 23: Flutter lấy Thông báo từ Backend

Trong `announcements_screen.dart`:

- Đổi từ `StatelessWidget` sang `StatefulWidget`
- Gọi API `GET /api/announcements`
- Có loading
- Có lỗi kết nối
- Có nút Thử lại
- Có kéo xuống refresh

---

## Bước 24: Tạo API Ca trực

Backend API:

```text
GET /api/shifts
```

Ban đầu trả dữ liệu cứng. Sau này đã đổi sang lấy từ SQLite.

---

## Bước 25: Flutter lấy Ca trực từ Backend

Trong `shifts_screen.dart`:

- Gọi API `GET /api/shifts`
- Hiển thị danh sách ca trực từ backend

---

## Bước 26: Tạo API Tài liệu

Backend API:

```text
GET /api/documents
```

Ban đầu trả dữ liệu cứng. Sau này đã đổi sang lấy từ SQLite.

---

## Bước 27: Flutter lấy Tài liệu từ Backend

Trong `documents_screen.dart`:

- Gọi API `GET /api/documents`
- Hiển thị tài liệu từ backend

---

## Bước 28: Tạo API Cá nhân

Backend API:

```text
GET /api/profile
```

Ban đầu trả dữ liệu cứng. Sau này đã đổi sang lấy từ SQLite.

---

## Bước 29: Flutter lấy Cá nhân từ Backend

Trong `profile_screen.dart`:

- Gọi API `GET /api/profile`
- Hiển thị thông tin nhân viên từ backend

---

## Bước 30: Tạo API Báo cáo sự cố

Model:

```python
class IncidentRequest(BaseModel):
    title: str
    location: str
    level: str
    description: str
```

API:

```text
POST /api/incidents
```

Ban đầu chỉ nhận và trả response mẫu. Sau này đã đổi sang lưu vào SQLite.

---

## Bước 31: Flutter gửi Báo cáo sự cố lên Backend

Trong `incident_report_screen.dart`:

- Gửi POST đến `/api/incidents`
- Body gồm `title`, `location`, `level`, `description`
- Có loading
- Có thông báo gửi thành công/thất bại

---

## Bước 32: Tạo SQLite Database

Tạo file:

```text
database.py
init_db.py
airport.db
```

`database.py` hiện nên dùng đường dẫn tuyệt đối:

```python
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "airport.db")


def get_db_connection():
    print("Using database:", DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
```

`init_db.py` tạo các bảng:

```text
users
announcements
shifts
documents
incidents
```

Chạy:

```powershell
python init_db.py
```

---

## Bước 33: API Thông báo lấy từ SQLite

Thay API `/api/announcements` thành:

```python
@app.get("/api/announcements")
def get_announcements():
    conn = get_db_connection()

    announcements = conn.execute("""
        SELECT id, title, content, date
        FROM announcements
        ORDER BY id ASC
    """).fetchall()

    conn.close()

    return [dict(item) for item in announcements]
```

Đã sửa lỗi `sqlite3.OperationalError: no such table: announcements` bằng cách dùng `DB_PATH` tuyệt đối trong `database.py`.

---

## Bước 34: API Ca trực lấy từ SQLite

```python
@app.get("/api/shifts")
def get_shifts():
    conn = get_db_connection()

    shifts = conn.execute("""
        SELECT id, date, time, department, location, status
        FROM shifts
        ORDER BY id ASC
    """).fetchall()

    conn.close()

    return [dict(item) for item in shifts]
```

---

## Bước 35: API Tài liệu lấy từ SQLite

```python
@app.get("/api/documents")
def get_documents():
    conn = get_db_connection()

    documents = conn.execute("""
        SELECT id, title, category, content
        FROM documents
        ORDER BY id ASC
    """).fetchall()

    conn.close()

    return [dict(item) for item in documents]
```

---

## Bước 36: API Cá nhân lấy từ SQLite

```python
@app.get("/api/profile")
def get_profile():
    conn = get_db_connection()

    user = conn.execute("""
        SELECT id, username, full_name, role, department
        FROM users
        WHERE id = 1
    """).fetchone()

    conn.close()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy nhân viên"
        )

    return {
        "id": user["id"],
        "name": user["full_name"],
        "code": "EMP001",
        "department": user["department"],
        "position": "Nhân viên an ninh",
        "phone": "0901000001",
        "email": "an.nguyen@airport.local"
    }
```

---

## Bước 37: API Đăng nhập lấy từ SQLite

```python
@app.post("/api/auth/login")
def login(data: LoginRequest):
    conn = get_db_connection()

    user = conn.execute("""
        SELECT id, username, password, full_name, role, department
        FROM users
        WHERE username = ?
    """, (data.username,)).fetchone()

    conn.close()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Sai tài khoản hoặc mật khẩu"
        )

    if user["password"] != data.password:
        raise HTTPException(
            status_code=401,
            detail="Sai tài khoản hoặc mật khẩu"
        )

    return {
        "success": True,
        "message": "Đăng nhập thành công",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "full_name": user["full_name"],
            "role": user["role"],
            "department": user["department"]
        }
    }
```

---

## Bước 38: Lưu Báo cáo sự cố vào SQLite

```python
@app.post("/api/incidents")
def create_incident(data: IncidentRequest):
    conn = get_db_connection()

    cursor = conn.execute("""
        INSERT INTO incidents (
            title,
            location,
            level,
            description,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        data.title,
        data.location,
        data.level,
        data.description,
        "Đã tiếp nhận"
    ))

    conn.commit()

    incident_id = cursor.lastrowid

    conn.close()

    return {
        "success": True,
        "message": "Đã nhận báo cáo sự cố",
        "incident": {
            "id": incident_id,
            "title": data.title,
            "location": data.location,
            "level": data.level,
            "description": data.description,
            "status": "Đã tiếp nhận"
        }
    }
```

Lưu ý khi test Swagger: phải test đúng API `POST /api/incidents`, không phải `POST /api/auth/login`.

---

## Bước 39: Tạo API xem danh sách sự cố

```python
@app.get("/api/incidents")
def get_incidents():
    conn = get_db_connection()

    incidents = conn.execute("""
        SELECT id, title, location, level, description, status
        FROM incidents
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return [dict(item) for item in incidents]
```

---

## Bước 40: Tạo màn hình Danh sách sự cố trong Flutter

Tạo file:

```text
lib/screens/incidents_screen.dart
```

Chức năng:

- Gọi API `GET /api/incidents`
- Hiển thị danh sách sự cố
- Có nút `+` để mở `IncidentReportScreen`
- Sau khi gửi sự cố, danh sách tự refresh

Trong `dashboard_screen.dart`, đổi ô Sự cố từ mở `IncidentReportScreen` sang mở `const IncidentsScreen()`.

---

## Bước 41: Gửi sự cố xong tự quay về danh sách

Trong `incident_report_screen.dart`, sau khi gửi thành công:

```dart
Navigator.pop(context, true);
```

Đã sửa lỗi `else` bị sai cấu trúc bằng cách thay lại toàn bộ hàm `submitIncident()`.

---

## Bước 42: Tạo file cấu hình API chung

Tạo file:

```text
lib/config/api_config.dart
```

Nội dung:

```dart
class ApiConfig {
  static const String baseUrl = 'http://192.168.10.190:8000';
}
```

Sau đó các file Flutter dùng:

```dart
import '../config/api_config.dart';

final String apiBaseUrl = ApiConfig.baseUrl;
```

Các file đã sửa:

```text
login_screen.dart
announcements_screen.dart
shifts_screen.dart
documents_screen.dart
profile_screen.dart
incident_report_screen.dart
incidents_screen.dart
```

---

## Bước 43: Tạo API Chatbot trên Backend

Model:

```python
class ChatbotRequest(BaseModel):
    question: str
```

API:

```python
@app.post("/api/chatbot/ask")
def ask_chatbot(data: ChatbotRequest):
    question = data.question.lower().strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Câu hỏi không được để trống"
        )

    if "hành lý" in question or "hanh ly" in question:
        answer = (
            "Khi nhận thông tin hành lý thất lạc, nhân viên cần lập biên bản, "
            "kiểm tra mã hành lý và liên hệ bộ phận liên quan."
        )
    elif "an ninh" in question or "thẻ" in question or "the" in question:
        answer = (
            "Nhân viên phải xuất trình thẻ khi vào khu vực hạn chế. "
            "Không cho mượn thẻ dưới mọi hình thức."
        )
    elif "sự cố" in question or "su co" in question:
        answer = (
            "Mọi sự cố trong quá trình khai thác phải được báo cáo ngay "
            "cho trưởng ca và ghi nhận vào hệ thống."
        )
    elif "ca trực" in question or "ca truc" in question:
        answer = (
            "Bạn có thể xem lịch ca trực trong mục Ca trực trên ứng dụng."
        )
    else:
        answer = (
            "Tôi chưa có đủ dữ liệu để trả lời câu hỏi này. "
            "Sau này phần chatbot sẽ được kết nối với tài liệu PDF nội bộ bằng RAG."
        )

    return {
        "answer": answer
    }
```

---

## Bước 44: Flutter Chatbot gọi Backend API

Trong `chatbot_screen.dart`:

- Gọi API `POST /api/chatbot/ask`
- Gửi body `question`
- Hiển thị câu trả lời từ backend
- Có trạng thái `Đang trả lời...`

---

## Bước 45: Tạo `requirements.txt`

Trong backend:

```powershell
cd C:\Users\PC\airport_backend
venv\Scripts\activate
pip freeze > requirements.txt
```

Dùng để cài lại thư viện sau này:

```powershell
pip install -r requirements.txt
```

---

## Bước 46: Tạo README

README này dùng để ghi lại:

- Cách chạy Backend
- Cách chạy Flutter
- Tài khoản demo
- IP backend
- API hiện có
- Lỗi thường gặp
- Hướng phát triển tiếp
- Toàn bộ các bước đã làm

---

# 9. Cách chạy mỗi ngày

## Terminal 1: Chạy Backend

```powershell
cd C:\Users\PC\airport_backend
venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Không tắt terminal này.

---

## Terminal 2: Chạy Flutter

```powershell
cd C:\Users\PC\airport_mobile_app
flutter devices
flutter run -d R5CX40LFFQD
```

Nếu Flutter bị thoát:

```powershell
cd C:\Users\PC\airport_mobile_app
flutter run -d R5CX40LFFQD
```

---

# 10. API hiện có

## Home

```text
GET /
```

## Health Check

```text
GET /api/health
```

## Đăng nhập

```text
POST /api/auth/login
```

Body:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

## Thông báo

```text
GET /api/announcements
```

## Ca trực

```text
GET /api/shifts
```

## Tài liệu

```text
GET /api/documents
```

## Cá nhân

```text
GET /api/profile
```

## Sự cố

```text
GET /api/incidents
POST /api/incidents
```

Body POST:

```json
{
  "title": "Sự cố tại khu vực check-in",
  "location": "Khu vực check-in",
  "level": "Quan trọng",
  "description": "Mô tả chi tiết sự cố"
}
```

## Chatbot

```text
POST /api/chatbot/ask
```

Body:

```json
{
  "question": "Quy trình xử lý hành lý thất lạc là gì?"
}
```

---

# 11. Database

File database:

```text
C:\Users\PC\airport_backend\airport.db
```

Các bảng:

```text
users
announcements
shifts
documents
incidents
```

---

# 12. Tạo lại database

```powershell
cd C:\Users\PC\airport_backend
venv\Scripts\activate
python init_db.py
```

Nếu muốn xóa database cũ:

```powershell
del airport.db
python init_db.py
```

---

# 13. Cài lại backend trên máy khác

```powershell
cd C:\Users\PC\airport_backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

# 14. Lỗi thường gặp

## 14.1. Flutter không thấy điện thoại

```powershell
flutter devices
```

Nếu không thấy:

- Rút dây USB
- Cắm lại
- Mở khóa điện thoại
- Bấm Allow USB Debugging
- Chạy lại `flutter devices`

## 14.2. Lost connection to device

Chạy lại:

```powershell
cd C:\Users\PC\airport_mobile_app
flutter run -d R5CX40LFFQD
```

## 14.3. Không kết nối được Backend API

Kiểm tra:

```text
http://127.0.0.1:8000
```

Trên điện thoại:

```text
http://192.168.10.190:8000
```

Nếu không được:

- Kiểm tra backend có chạy chưa
- Kiểm tra điện thoại và máy tính cùng Wi-Fi
- Kiểm tra IP trong `api_config.dart`
- Kiểm tra firewall
- Chạy backend bằng `--host 0.0.0.0`

## 14.4. IP máy tính đổi

Chạy:

```powershell
ipconfig
```

Sửa file:

```text
lib/config/api_config.dart
```

Ví dụ:

```dart
class ApiConfig {
  static const String baseUrl = 'http://192.168.1.50:8000';
}
```

## 14.5. Backend báo `no such table`

Chạy lại:

```powershell
cd C:\Users\PC\airport_backend
venv\Scripts\activate
python init_db.py
```

Nếu vẫn lỗi:

```powershell
del airport.db
python init_db.py
```

## 14.6. `uvicorn` is not recognized

Chạy đúng thư mục backend và kích hoạt venv:

```powershell
cd C:\Users\PC\airport_backend
venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

# 15. Chức năng hiện tại

Mobile App đã có:

```text
Đăng nhập
Trang chủ
Thông báo
Ca trực
Tài liệu
Cá nhân
Danh sách sự cố
Báo cáo sự cố
Chatbot
```

Backend đã có:

```text
FastAPI
SQLite database
API đăng nhập
API thông báo
API ca trực
API tài liệu
API cá nhân
API gửi báo cáo sự cố
API xem danh sách sự cố
API chatbot đơn giản
```

---

# 16. Trạng thái hiện tại

Đã hoàn thành:

```text
Mobile App Flutter chạy trên điện thoại thật
Backend FastAPI chạy trên máy tính
SQLite database
Mobile gọi được Backend API
Backend đọc/ghi được SQLite
Chatbot gọi Backend API
Báo cáo sự cố lưu được database
```

Trạng thái:

```text
Demo nội bộ đã chạy được end-to-end.
```

---

# 17. Việc nên làm tiếp theo

Thứ tự phát triển tiếp đề xuất:

```text
1. Tạo Admin Web
2. Thêm API thêm/sửa/xóa thông báo
3. Thêm API thêm/sửa/xóa ca trực
4. Thêm API quản lý tài liệu
5. Thêm phân quyền admin/employee
6. Mã hóa mật khẩu bằng hash
7. Thêm JWT token đăng nhập
8. Thêm upload PDF
9. Tích hợp RAG chatbot đọc PDF
10. Build APK Android
11. Chạy backend ổn định bằng server nội bộ
12. Chuyển SQLite sang PostgreSQL nếu triển khai thật
```

---

# 18. Ghi chú bảo mật

Bản hiện tại là demo/học tập.

Chưa nên dùng thật cho môi trường sản xuất vì:

```text
Mật khẩu đang lưu dạng text
Chưa có JWT token
Chưa có phân quyền chặt chẽ
Chưa có HTTPS
Chưa có backup database tự động
Chưa có tài khoản admin riêng
```

Trước khi triển khai thật cần nâng cấp bảo mật.

---

# 19. File quan trọng cần backup

Nên backup:

```text
C:\Users\PC\airport_mobile_app
C:\Users\PC\airport_backend
```

Quan trọng nhất:

```text
airport_backend/airport.db
airport_backend/main.py
airport_backend/database.py
airport_backend/init_db.py
airport_backend/requirements.txt
airport_mobile_app/lib/
airport_mobile_app/pubspec.yaml
```

Không bắt buộc backup:

```text
airport_backend/venv/
airport_mobile_app/build/
```

vì có thể tạo lại.
