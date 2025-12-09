from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models import User
from app.auth import get_password_hash

def seed():
    create_db_and_tables()
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == "admin")).first()
        if not user:
            user = User(username="admin", password_hash=get_password_hash("password"))
            session.add(user)
            session.commit()
            print("User 'admin' created with password 'password'")
        else:
            print("User 'admin' already exists")

if __name__ == "__main__":
    seed()
