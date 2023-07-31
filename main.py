from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from client import Client

app = FastAPI()

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@db/postgres'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


client = Client()


class Table(Base):
    __tablename__ = 'test'

    uuid = Column(String, primary_key=True)
    text = Column(String)


Base.metadata.create_all(bind=engine)


class CreateEntry(BaseModel):
    uuid: str
    text: str


class EntryResponse(BaseModel):
    uuid: str
    text: str


class EntryResponseList(BaseModel):
    entries: List[EntryResponse]


@app.post("/new")
def create_entry(request: List[CreateEntry]):
    postgres_db = SessionLocal()

    for item in request:
        entry = Table(uuid=item.uuid, text=item.text)
        postgres_db.add(entry)

    postgres_db.commit()

    return {"message": "New entry created successfully"}


@app.get("/all", response_model=EntryResponseList)
def get_all_entries():
    postgres_db = SessionLocal()
    entries = postgres_db.query(Table).all()
    return {"Entries": entries}


@app.get("/{uuid}", response_model=EntryResponse)
def get_entry(uuid: str):
    postgres_db = SessionLocal()
    entry = postgres_db.query(Table).filter(uuid == Table.uuid).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    return entry


@app.get("/count/{count}", response_model=EntryResponseList)
def get_some_entries(count: int):
    postgres_db = SessionLocal()
    entries = postgres_db.query(Table).limit(count).all()
    return {"Entries": entries}


@app.delete("/{uuid}")
def delete_entry(uuid: str):
    postgres_db = SessionLocal()
    entry = postgres_db.query(Table).filter(uuid == Table.uuid).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    postgres_db.delete(entry)
    postgres_db.commit()

    return {"message": "Entry deleted successfully"}


client.start_client()
