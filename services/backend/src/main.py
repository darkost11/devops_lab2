# main.py
from contextlib import asynccontextmanager
from datetime import datetime
from typing import ClassVar, final

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, DateTime, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

from src.config import AppSettings
from src.database import database

Base = declarative_base()


# Модель базы данных
@final
class NoteDB(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    note = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)


# Модель Pydantic для валидации данных запроса
class NoteCreate(BaseModel):
    note: str


class NoteResponse(BaseModel):
    id: int
    note: str
    date: datetime

    config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


# Разрешенные источники
origins = [
    "*",  # URL фронтенда
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = AppSettings()
    database.setup(config=config)
    engine = database.async_engine
    if not engine:
        raise RuntimeError("need setup first")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await database.shutdown()


app = FastAPI(lifespan=lifespan)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Маршрут для получения всех заметок
@app.get("/notes", response_model=list[NoteResponse])
async def get_notes(
    session: AsyncSession = Depends(database),
):
    result = await session.execute(select(NoteDB))
    notes = result.scalars().all()
    return notes


# Маршрут для добавления новой заметки
@app.post("/notes", response_model=NoteResponse)
async def create_note(
    note: NoteCreate,
    session: AsyncSession = Depends(database),
):
    db_note = NoteDB(note=note.note)
    async with session.begin():
        session.add(db_note)
    await session.refresh(db_note)
    return db_note
