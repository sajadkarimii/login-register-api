from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

engine = create_async_engine("mysql+aiomysql://root:s2233943j@localhost:3306/profile")

SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

class Base(DeclarativeBase, MappedAsDataclass):
    pass

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()