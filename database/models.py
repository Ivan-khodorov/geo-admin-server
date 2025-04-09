from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import (
    String, Integer, Float, Boolean, ForeignKey,
    DateTime, Text, JSON, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime
from datetime import datetime


class Base(AsyncAttrs, DeclarativeBase):
    pass


# 👤 Сотрудник / Админ / Менеджер
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[str] = mapped_column(String(64), unique=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[str] = mapped_column(String(16), default="worker")  # worker | admin | manager
    city: Mapped[str] = mapped_column(String(128), nullable=True)

    routes: Mapped[list["Route"]] = relationship(back_populates="user")
    photos: Mapped[list["PointPhoto"]] = relationship(back_populates="user")



# 📆 Маршрут (привязан к пользователю и дате)
class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="routes")
    points: Mapped[list["Point"]] = relationship(back_populates="route")


# 📍 Точка маршрута (подъезд)
class Point(Base):
    __tablename__ = "points"

    id: Mapped[int] = mapped_column(primary_key=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"))
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    lat: Mapped[float] = mapped_column()
    lon: Mapped[float] = mapped_column()
    flyer_count: Mapped[int] = mapped_column(default=0)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    sub_points: Mapped[list["SubPoint"]] = relationship(back_populates="point", cascade="all, delete-orphan")

    route: Mapped["Route"] = relationship(back_populates="points")
    photos: Mapped[list["PointPhoto"]] = relationship(back_populates="point")

# 🚪 Подточка (подъезд) внутри точки-дома
class SubPoint(Base):
    __tablename__ = "sub_points"

    id: Mapped[int] = mapped_column(primary_key=True)
    point_id: Mapped[int] = mapped_column(ForeignKey("points.id"))
    entrance_number: Mapped[int] = mapped_column()  # 1, 2, 3, 4
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    point: Mapped["Point"] = relationship(back_populates="sub_points")
    photos: Mapped[list["SubPointPhoto"]] = relationship(back_populates="sub_point", cascade="all, delete-orphan")

# 🖼 Фотофиксация на точке
class PointPhoto(Base):
    __tablename__ = "point_photos"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    point_id: Mapped[int] = mapped_column(ForeignKey("points.id"))
    filepath: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="photos")
    point: Mapped["Point"] = relationship(back_populates="photos")

# 🖼 Фотофиксация для подъезда
class SubPointPhoto(Base):
    __tablename__ = "sub_point_photos"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    sub_point_id: Mapped[int] = mapped_column(ForeignKey("sub_points.id"))
    filepath: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship()
    sub_point: Mapped["SubPoint"] = relationship(back_populates="photos")

# 📊 Ежедневный отчёт
class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    completed_points: Mapped[int] = mapped_column()
    total_points: Mapped[int] = mapped_column()
    notes: Mapped[str] = mapped_column(Text)

    user: Mapped["User"] = relationship()


# 🗺 Область на карте, отрисованная админом
class CityZone(Base):
    __tablename__ = "city_zones"
    id: Mapped[int] = mapped_column(primary_key=True)
    city_name: Mapped[str] = mapped_column(String(128), nullable=False)
    polygon_coords: Mapped[list] = mapped_column(JSON, nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    houses: Mapped[list["House"]] = relationship(back_populates="zone", cascade="all, delete-orphan")


# 🏠 Дом внутри зоны
class House(Base):
    __tablename__ = "houses"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_zone_id: Mapped[int] = mapped_column(ForeignKey("city_zones.id"))
    address: Mapped[str] = mapped_column(String(256), nullable=False)
    lat: Mapped[float] = mapped_column(nullable=False)
    lon: Mapped[float] = mapped_column(nullable=False)
    is_visited: Mapped[bool] = mapped_column(Boolean, default=False)

    zone: Mapped["CityZone"] = relationship(back_populates="houses")

class FailedAttempt(Base):
    __tablename__ = "failed_attempts"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    point_id = mapped_column(ForeignKey("points.id"), nullable=True)
    attempt_lat = mapped_column(Float, nullable=False)
    attempt_lon = mapped_column(Float, nullable=False)
    distance_meters = mapped_column(Float)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    point = relationship("Point")