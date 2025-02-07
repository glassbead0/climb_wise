from sqlalchemy.orm import Mapped, mapped_column
from base import Base

class Waypoint(Base):
    __tablename__ = 'waypoints'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=True)
    notes: Mapped[str] = mapped_column(nullable=True)
    latitude: Mapped[float] = mapped_column(nullable=True)
    longitude: Mapped[float] = mapped_column(nullable=True)
    elevation: Mapped[int] = mapped_column(nullable=True)
    marker_color: Mapped[str] = mapped_column(nullable=True)
    geometry: Mapped[Geometry] = mapped_column(Geometry('POINT', srid=4326))
    created_at: Mapped[Optional[TIMESTAMP]] = mapped_column(TIMESTAMP, default='now()')
    # trail_id: Mapped[int] = mapped_column(ForeignKey('trails.id', ondelete='CASCADE'))
    # trail: Mapped["Trail"] = relationship("Trail", back_populates="waypoints")