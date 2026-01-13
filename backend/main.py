from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import init_db
from routes import auth, tasks, dashboard

app = FastAPI(title="Task Web App API")

# Frontend origins (Next.js running on 3000/3001/3007 during dev)
origins = [
    "http://localhost:3007",
    "http://127.0.0.1:3007",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Task API Running"}

# Routes
app.include_router(auth.router)
app.include_router(auth.better_auth_router)
app.include_router(tasks.router)
app.include_router(dashboard.router)
