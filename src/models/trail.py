from sqlalchemy.orm import Mapped, mapped_column
from base import Base

class Trail(Base):
    '''
    Represents a trail that has been imported from GaiaGPS
    '''
    __tablename__ = 'trails'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=True)
    color: Mapped[str] = mapped_column(nullable=True)
    hexcolor: Mapped[str] = mapped_column(nullable=True)
    notes: Mapped[str] = mapped_column(nullable=True)
    track_type: Mapped[str] = mapped_column(nullable=True)
    routing_mode: Mapped[str] = mapped_column(nullable=True)
    distance: Mapped[float] = mapped_column(nullable=True)
    total_ascent: Mapped[float] = mapped_column(nullable=True)
    total_descent: Mapped[float] = mapped_column(nullable=True)
    stopped_time: Mapped[float] = mapped_column(nullable=True)
    total_time: Mapped[float] = mapped_column(nullable=True)
    average_speed: Mapped[float] = mapped_column(nullable=True)
    moving_time: Mapped[float] = mapped_column(nullable=True)
    moving_speed: Mapped[float] = mapped_column(nullable=True)
    activities: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    latitude: Mapped[float] = mapped_column(nullable=True)
    longitude: Mapped[float] = mapped_column(nullable=True)
    geometry: Mapped[Geometry] = mapped_column(Geometry('MULTILINESTRINGZ', dimension=3, srid=4326))
    created_at: Mapped[Optional[TIMESTAMP]] = mapped_column(TIMESTAMP, default='now()')
    # waypoints: Mapped[List["Waypoint"]] = relationship("Waypoint", back_populates="trail", cascade="all, delete-orphan")
