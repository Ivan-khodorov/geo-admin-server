# webapp-project/schema_loader.py
from fastapi import APIRouter
from sqlalchemy import text
from database.session import engine  # тот же engine, что и у проекта

router = APIRouter()

@router.post("/import-schema")
async def import_schema():
    try:
        with open("database_schema.sql", "r", encoding="utf-8") as f:
            raw_sql = f.read()

        async with engine.begin() as conn:
            for statement in raw_sql.split(";"):
                stmt = statement.strip()
                if stmt:
                    await conn.execute(text(stmt))
        return {"status": "✅ Schema imported successfully"}

    except Exception as e:
        return {"status": "❌ Failed", "error": str(e)}