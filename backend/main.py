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



# main.py ke routes ko exactly aise replace karein
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/dashboard/tasks", tags=["Tasks"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(chat.router, prefix="/conversations", tags=["Conversations"])