from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db_and_tables
from .routers import auth, incidents, stats

app = FastAPI(
    title="Codeflow Management API",
    description="API for Incident Management and Churn Prediction",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "https://managment.codeflowcapital.online",
    "http://managment.codeflowcapital.online",
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
    create_db_and_tables()

app.include_router(auth.router)
app.include_router(incidents.router)
app.include_router(stats.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Codeflow Management API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

