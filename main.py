from fastapi import FastAPI
from schema_loader import router as schema_router

app = FastAPI()

app.include_router(schema_router)