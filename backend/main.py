from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import init_db
from routes import auth, tasks, dashboard, chat

app = FastAPI(title="Task Web App API", version="1.0.0")

# CORS CONFIG
origins = ["*"] # Development ke liye simplify kar diya taake connectivity issue na aaye

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

# ROUTES
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/dashboard/tasks", tags=["Tasks"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])