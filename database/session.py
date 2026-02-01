from sqlmodel import Session
from sqlalchemy import create_engine
from sqlmodel import SQLModel
from typing import Annotated
from fastapi import Depends
engine=create_engine(
    url="sqlite:///sqlite.db",
    echo=True,
    connect_args={
        "check_same_thread":False
    }
)


from .models import Shipment
def create_db_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(bind=engine) as session:
        yield session


sessionDep= Annotated[Session,Depends(get_session)]