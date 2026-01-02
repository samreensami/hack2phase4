from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import init_db
from .core.config import settings
from .routes import auth, tasks

app = FastAPI(title="Task Web App API")

# Configure CORS
origins = [
    "http://localhost:3000",  # Local Next.js
    "https://your-production-frontend.vercel.app",  # TODO: Replace with real URL
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
def read_root():
    return {"message": "Welcome to Task Web App API"}

app.include_router(auth.router)
app.include_router(tasks.router)
