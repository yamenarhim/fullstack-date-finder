from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, Integer, String, Text
from datetime import datetime

# Async SQLite URL
DATABASE_URL = "sqlite+aiosqlite:///./logs.db"

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

# The Log Model
class APIRequestLog(Base):
    __tablename__ = "api_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    method: Mapped[str] = mapped_column(String(10))
    path: Mapped[str] = mapped_column(String(255))
    query_params: Mapped[str] = mapped_column(Text, nullable=True)
    status_code: Mapped[int] = mapped_column(Integer)
    process_time_ms: Mapped[float] = mapped_column(Integer) # In milliseconds
    client_ip: Mapped[str] = mapped_column(String(50))

# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Helper to init DB tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)