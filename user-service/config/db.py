import os
from sqlmodel import SQLModel, create_engine, Session



DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)
    print("Database created")


def get_session():
    with Session(engine) as session:
        yield session
