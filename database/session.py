import os

DATABASE_URL = os.environ["DATABASE_URL"]

# Асинхронная сессия
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)