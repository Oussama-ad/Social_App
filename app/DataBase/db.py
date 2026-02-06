from collections.abc import AsyncGenerator
import uuid
import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship

DB_URL = "postgresql+asyncpg://postgres:My_Db_1.2.3.4@localhost:5432/postgres"

# schema part 
class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__="posts"
    id = Column(UUID(as_uuid=True), primary_key=True , default=uuid.uuid4)
    Caption = Column(Text)
    url_image=Column(String , nullable=False) # nullable=false means that this one can not be null it is mendatory 
    file_type= Column(String,nullable=False)
    file_name = Column(String,nullable=False)
    created_at = Column(DateTime,default=datetime.datetime.now)

engine = create_async_engine(DB_URL)  
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)  

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
