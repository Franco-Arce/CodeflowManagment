from sqlmodel import SQLModel, create_engine, Session
import os

# Fallback to SQLite if no DATABASE_URL env var (e.g. running locally without Docker)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./codeflow.db")

if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
