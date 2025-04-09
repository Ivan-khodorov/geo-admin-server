from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.Config import Config

# Создаём асинхронный движок
engine = create_async_engine(Config.DATABASE_URL, echo=True)

# Асинхронная сессия
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)