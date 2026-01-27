from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import init_db
from routes import auth, tasks, dashboard, chat

app = FastAPI(title="Task Web App API", version="1.0.0")

# CORS CONFIG - Allow everything for development
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# STARTUP: Database tables banata hai
@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"status": "success", "message": "Task API Running"}

# ROUTES - Frontend ki requests se match karne ke liye /api prefix laazmi hai
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/api/dashboard/tasks", tags=["Tasks"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])

# Chatbot ke liye ye dono prefixes zaroori hain
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(chat.router, prefix="/api/conversations", tags=["Conversations"])