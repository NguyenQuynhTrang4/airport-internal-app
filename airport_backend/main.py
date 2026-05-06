from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_db_connection

app = FastAPI(title="Airport Internal Backend API")
class LoginRequest(BaseModel):
    username: str
    password: str
    
class IncidentRequest(BaseModel):
    title: str
    location: str
    level: str
    description: str  
    
class ChatbotRequest(BaseModel):
    question: str      


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