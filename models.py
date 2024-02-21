import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncAttrs, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'flask123'
POSTGRES_DB = 'app_flask_aiohttp'
POSTGRES_HOST = '127.0.0.1'
POSTGRES_PORT = '5432'

PG_DSN = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Announcement(Base):
    __tablename__ = 'user_announcement'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    date_of_creation: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner: Mapped[str] = mapped_column(String(100), index=True, nullable=True)

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'date_of_creation': self.date_of_creation.isoformat()

        }


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
