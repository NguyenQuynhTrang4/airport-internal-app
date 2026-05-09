import os
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.templating import Jinja2Templates
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware

from database import get_db_connection

app = FastAPI(title="Airport Internal Backend API")

app.add_middleware(
    SessionMiddleware,
    secret_key="airport-admin-session-secret-change-this-later"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "airport-internal-secret-key-change-this-later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
security = HTTPBearer()
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Token không hợp lệ"
            )

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token không hợp lệ hoặc đã hết hạn"
        )

    conn = get_db_connection()

    user = conn.execute("""
        SELECT id, username, full_name, role, department
        FROM users
        WHERE username = ?
    """, (username,)).fetchone()

    conn.close()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Không tìm thấy người dùng"
        )

    return dict(user)
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

    if not pwd_context.verify(data.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Sai tài khoản hoặc mật khẩu"
        )

    access_token = create_access_token(
    data={
        "sub": user["username"],
        "user_id": user["id"],
        "role": user["role"]
        }
    )

    return {
        "success": True,
        "message": "Đăng nhập thành công",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "full_name": user["full_name"],
            "role": user["role"],
            "department": user["department"]
        }
    }   
   
@app.get("/api/announcements")
def get_announcements(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()

    announcements = conn.execute("""
        SELECT id, title, content, date
        FROM announcements
        ORDER BY id ASC
    """).fetchall()

    conn.close()

    return [dict(item) for item in announcements]   
    
@app.get("/api/shifts")
def get_shifts(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()

    shifts = conn.execute("""
        SELECT id, date, time, department, location, status
        FROM shifts
        ORDER BY id ASC
    """).fetchall()

    conn.close()

    return [dict(item) for item in shifts]
    
@app.get("/api/documents")
def get_documents(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()

    documents = conn.execute("""
        SELECT id, title, category, content
        FROM documents
        ORDER BY id ASC
    """).fetchall()

    conn.close()

    return [dict(item) for item in documents]
    
@app.get("/api/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()

    user = conn.execute("""
        SELECT id, username, full_name, role, department
        FROM users
        WHERE id = ?
    """, (current_user["id"],)).fetchone()

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
def create_incident(
    data: IncidentRequest,
    current_user: dict = Depends(get_current_user)
):
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
def get_incidents(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()

    incidents = conn.execute("""
        SELECT id, title, location, level, description, status
        FROM incidents
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return [dict(item) for item in incidents] 

@app.post("/api/chatbot/ask")
def ask_chatbot(
    data: ChatbotRequest,
    current_user: dict = Depends(get_current_user)
):
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
    
def require_admin_session(request: Request):
    admin_user = request.session.get("admin_user")

    if admin_user is None:
        return None

    if admin_user.get("role") != "admin":
        return None

    return admin_user


@app.get("/admin")
def admin_dashboard(request: Request):
    admin_user = require_admin_session(request)

    if admin_user is None:
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )

    conn = get_db_connection()

    announcement_count = conn.execute(
        "SELECT COUNT(*) AS count FROM announcements"
    ).fetchone()["count"]

    shift_count = conn.execute(
        "SELECT COUNT(*) AS count FROM shifts"
    ).fetchone()["count"]

    document_count = conn.execute(
        "SELECT COUNT(*) AS count FROM documents"
    ).fetchone()["count"]

    incident_count = conn.execute(
        "SELECT COUNT(*) AS count FROM incidents"
    ).fetchone()["count"]

    conn.close()

    return templates.TemplateResponse(
        request,
        "admin/admin_dashboard.html",
        {
            "announcement_count": announcement_count,
            "shift_count": shift_count,
            "document_count": document_count,
            "incident_count": incident_count,
        }
    )    
    
@app.get("/admin/incidents")
def admin_incidents(request: Request):
    admin_user = require_admin_session(request)

    if admin_user is None:
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )
    conn = get_db_connection()

    incidents = conn.execute("""
        SELECT id, title, location, level, description, status
        FROM incidents
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return templates.TemplateResponse(
        request,
        "admin/admin_incidents.html",
        {
            "incidents": incidents
        }
    )   
    
@app.post("/admin/incidents/{incident_id}/status")
def update_incident_status(
    request: Request,
    incident_id: int,
    status: str = Form(...)
):
    admin_user = require_admin_session(request)

    if admin_user is None:
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )
    conn = get_db_connection()

    conn.execute("""
        UPDATE incidents
        SET status = ?
        WHERE id = ?
    """, (status, incident_id))

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/admin/incidents",
        status_code=303
    )    
    
@app.get("/admin/announcements")
def admin_announcements(request: Request):
    admin_user = require_admin_session(request)

    if admin_user is None:
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )
    conn = get_db_connection()

    announcements = conn.execute("""
        SELECT id, title, content, date
        FROM announcements
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return templates.TemplateResponse(
        request,
        "admin/admin_announcements.html",
        {
            "announcements": announcements
        }
    )


@app.post("/admin/announcements/create")
def create_admin_announcement(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    date: str = Form(...)
):
    admin_user = require_admin_session(request)

    if admin_user is None:
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )
    conn = get_db_connection()

    conn.execute("""
        INSERT INTO announcements (title, content, date)
        VALUES (?, ?, ?)
    """, (title, content, date))

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/admin/announcements",
        status_code=303
    )


@app.post("/admin/announcements/{announcement_id}/delete")
def delete_admin_announcement(
    request: Request,
    announcement_id: int
):
    admin_user = require_admin_session(request)

    if admin_user is None:
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )
    conn = get_db_connection()

    conn.execute("""
        DELETE FROM announcements
        WHERE id = ?
    """, (announcement_id,))

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/admin/announcements",
        status_code=303
    )
    
@app.get("/admin/shifts")
def admin_shifts(request: Request):
    admin_user = require_admin_session(request)

    if admin_user is None:
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )
    conn = get_db_connection()

    shifts = conn.execute("""
        SELECT id, date, time, department, location, status
        FROM shifts
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return templates.TemplateResponse(
        request,
        "admin/admin_shifts.html",
        {
            "shifts": shifts
        }
    )


@app.post("/admin/shifts/create")
def create_admin_shift(
    request: Request,
    date: str = Form(...),
    time: str = Form(...),
    department: str = Form(...),
    location: str = Form(...),
    status: str = Form(...)
):
    admin_user = require_admin_session(request)

    if admin_user is None:
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )
    conn = get_db_connection()

    conn.execute("""
        INSERT INTO shifts (
            date,
            time,
            department,
            location,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        date,
        time,
        department,
        location,
        status
    ))

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/admin/shifts",
        status_code=303
    )


@app.post("/admin/shifts/{shift_id}/delete")
def delete_admin_shift(
    request: Request,
    shift_id: int
):
    admin_user = require_admin_session(request)

    if admin_user is None:
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )
    conn = get_db_connection()

    conn.execute("""
        DELETE FROM shifts
        WHERE id = ?
    """, (shift_id,))

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/admin/shifts",
        status_code=303
    )  
    
@app.get("/admin/documents")
def admin_documents(request: Request):
    admin_user = require_admin_session(request)

    if admin_user is None:
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )
    conn = get_db_connection()

    documents = conn.execute("""
        SELECT id, title, category, content
        FROM documents
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return templates.TemplateResponse(
        request,
        "admin/admin_documents.html",
        {
            "documents": documents
        }
    )


@app.post("/admin/documents/create")
def create_admin_document(
    request: Request,
    title: str = Form(...),
    category: str = Form(...),
    content: str = Form(...)
):
    admin_user = require_admin_session(request)

    if admin_user is None:
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )
    conn = get_db_connection()

    conn.execute("""
        INSERT INTO documents (
            title,
            category,
            content
        )
        VALUES (?, ?, ?)
    """, (
        title,
        category,
        content
    ))

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/admin/documents",
        status_code=303
    )


@app.post("/admin/documents/{document_id}/delete")
def delete_admin_document(
    request: Request,
    document_id: int
):
    admin_user = require_admin_session(request)

    if admin_user is None:
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )
    conn = get_db_connection()

    conn.execute("""
        DELETE FROM documents
        WHERE id = ?
    """, (document_id,))

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/admin/documents",
        status_code=303
    )  
    
@app.get("/api/auth/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "success": True,
        "user": {
            "id": current_user["id"],
            "username": current_user["username"],
            "full_name": current_user["full_name"],
            "role": current_user["role"],
            "department": current_user["department"]
        }
    }
    
@app.get("/admin/login")
def admin_login_page(request: Request):
    return templates.TemplateResponse(
        request,
        "admin/admin_login.html",
        {
            "error": None
        }
    )


@app.post("/admin/login")
def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    conn = get_db_connection()

    user = conn.execute("""
        SELECT id, username, password, full_name, role, department
        FROM users
        WHERE username = ?
    """, (username,)).fetchone()

    conn.close()

    if user is None:
        return templates.TemplateResponse(
            request,
            "admin/admin_login.html",
            {
                "error": "Sai tài khoản hoặc mật khẩu"
            }
        )

    if not pwd_context.verify(password, user["password"]):
        return templates.TemplateResponse(
            request,
            "admin/admin_login.html",
            {
                "error": "Sai tài khoản hoặc mật khẩu"
            }
        )

    if user["role"] != "admin":
        return templates.TemplateResponse(
            request,
            "admin/admin_login.html",
            {
                "error": "Tài khoản không có quyền quản trị"
            }
        )

    request.session["admin_user"] = {
        "id": user["id"],
        "username": user["username"],
        "full_name": user["full_name"],
        "role": user["role"]
    }

    return RedirectResponse(
        url="/admin",
        status_code=303
    ) 
    
@app.get("/admin/logout")
def admin_logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url="/admin/login",
        status_code=303
    )       