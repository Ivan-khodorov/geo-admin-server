from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, CityZone, House
from database.session import async_session
from shapely.geometry import Polygon, Point
import json
import random

app = FastAPI()

# Разрешаем запросы с GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ivan-khodorov.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ZoneData(BaseModel):
    city: str
    zone: list  # [{lon: ..., lat: ...}, ...]

@app.post("/save-zone")
async def save_zone(data: ZoneData):
    polygon_coords = [(p["lon"], p["lat"]) for p in data.zone]
    polygon = Polygon(polygon_coords)

    async with async_session() as session:
        new_zone = CityZone(
            city_name=data.city,
            polygon_coords=data.zone,
            created_by=1
        )
        session.add(new_zone)
        await session.flush()

        bounds = polygon.bounds
        houses = []
        while len(houses) < 20:
            lon = random.uniform(bounds[0], bounds[2])
            lat = random.uniform(bounds[1], bounds[3])
            point = Point(lon, lat)
            if polygon.contains(point):
                address = f"Улица {random.randint(1, 99)}, д.{random.randint(1, 20)}"
                house = House(
                    address=address,
                    lat=lat,
                    lon=lon,
                    city=data.city,
                    city_zone_id=new_zone.id
                )
                houses.append(house)

        session.add_all(houses)
        await session.commit()

    return {"status": "ok", "saved": len(houses), "city": data.city}