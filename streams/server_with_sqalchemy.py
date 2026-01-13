import asyncio
from contextlib import asynccontextmanager
from typing import List, AsyncGenerator

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncAttrs
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# --- 1. Database Configuration ---
# In production, use "postgresql+asyncpg://..."
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create the Async Engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create the session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


# --- 2. Database Models (SQLAlchemy) ---
class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all DB models."""
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column()


# --- 3. Pydantic Schemas (Data Validation) ---
class UserCreate(BaseModel):
    username: str
    email: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    # Required for Pydantic to read data from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)


# --- 4. Application Lifecycle ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown logic."""
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Close engine
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


# --- 5. Dependency Injection ---
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provides a database session for a single request."""
    async with AsyncSessionLocal() as session:
        yield session


# --- 6. API Endpoints ---

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user asynchronously."""
    new_user = User(username=user.username, email=user.email)
    db.add(new_user)

    # 'commit' saves the transaction
    await db.commit()
    # 'refresh' reloads the object (to get the generated ID)
    await db.refresh(new_user)
    return new_user


@app.get("/users/", response_model=List[UserResponse])
async def read_users(db: AsyncSession = Depends(get_db)):
    """Fetch all users asynchronously."""
    # SQLAlchemy 2.0 Syntax: select(Model)
    query = select(User)

    # 'await' the execution of the query
    result = await db.execute(query)

    # scalars() gives us the User objects, all() converts to a list
    return result.scalars().all()


# --- Execution ---
if __name__ == "__main__":
    import uvicorn

    # Run using: python main.py
    uvicorn.run(app, host="127.0.0.1", port=8001)

    # go to http://127.0.0.1:800/docs to test it !!