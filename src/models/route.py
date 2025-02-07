from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import TIMESTAMP, func, Table
from datetime import datetime
from .base import Base

class Route(Base):
    '''
    A climbing Route on Mountain Project. pulled from https://www.kaggle.com/datasets/pdegner/mountain-project-rotues-and-forums?select=mp_routes.csv
    '''
    __tablename__ = 'routes'

    routeid: Mapped[int] = mapped_column(primary_key=True)
    route_name: Mapped[str] = mapped_column(nullable=False, default="?")
    location: Mapped[str] = mapped_column(nullable=True)
    url: Mapped[str] = mapped_column(nullable=True)
    avg_stars: Mapped[float] = mapped_column(nullable=True)
    route_type: Mapped[str] = mapped_column(nullable=True)
    alpine: Mapped[bool] = mapped_column(nullable=True)
    rating: Mapped[str] = mapped_column(nullable=True)
    safety: Mapped[str] = mapped_column(nullable=True)
    pitches: Mapped[int] = mapped_column(nullable=True)
    length: Mapped[int] = mapped_column(nullable=True)
    area_latitude: Mapped[float] = mapped_column(nullable=True)
    area_longitude: Mapped[float] = mapped_column(nullable=True)
    desc: Mapped[str] = mapped_column(nullable=True)
    protection: Mapped[str] = mapped_column(nullable=True)
    num_votes: Mapped[int] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now(), onupdate=func.now())

def route_table(engine):
    return Table(Route.__tablename__, Route.metadata, autoload_with=engine)