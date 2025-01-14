from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy import create_engine, String, ARRAY, TIMESTAMP
from typing import Optional
from geoalchemy2 import Geometry
import os

class Base(DeclarativeBase):
    pass

### For Mountain Project Data Importing ###

class Tick(Base):
    '''
    This is to hold the raw data pulled from MP for a specific user
    I transform this data into the TickedRoute table which is more useful.
    I could do away with this table entirely and simply keep the ticks_raw.csv file for reference :shrug:
    '''
    __tablename__ = 'ticks'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(nullable=True)
    route: Mapped[str] = mapped_column(nullable=True)
    rating: Mapped[str] = mapped_column(nullable=True)
    notes: Mapped[str] = mapped_column(nullable=True)
    url: Mapped[str] = mapped_column(nullable=True)
    pitches: Mapped[int] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(nullable=True)
    avg_stars: Mapped[float] = mapped_column(nullable=True)
    your_stars: Mapped[float] = mapped_column(nullable=True)
    style: Mapped[str] = mapped_column(nullable=True)
    lead_style: Mapped[str] = mapped_column(nullable=True)
    route_type: Mapped[str] = mapped_column(nullable=True)
    your_rating: Mapped[str] = mapped_column(nullable=True)
    length: Mapped[int] = mapped_column(nullable=True)
    rating_code: Mapped[int] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f'Tick(route={self.route})'
    
class TickedRoute(Base):
    '''
    Represents a route that has been ticked. the difference between this and the Tick table
    is that all ticks of the same route have been combined into a single Route row, with
    the "attempts" field to capture how many ticks that route has.
    This is distinct from the Route Table, which is a route listed on MP, regardless of whether
    it has been ticked or not.
    '''
    __tablename__ = 'ticked_routes'

    routeid: Mapped[int] = mapped_column(primary_key=True)
    route: Mapped[str]
    date: Mapped[str] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(nullable=True)
    route_type: Mapped[str] = mapped_column(nullable=True)
    alpine: Mapped[bool] = mapped_column(nullable=True)
    rating: Mapped[str] = mapped_column(nullable=True)
    safety: Mapped[str] = mapped_column(nullable=True)
    avg_stars: Mapped[float] = mapped_column(nullable=True)
    pitches: Mapped[int] = mapped_column(nullable=True)
    lead_style: Mapped[str] = mapped_column(nullable=True)
    attempts: Mapped[int] = mapped_column(nullable=True)

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
    rating: Mapped[str] = mapped_column(nullable=True)
    pitches: Mapped[int] = mapped_column(nullable=True)
    length: Mapped[int] = mapped_column(nullable=True)
    area_latitude: Mapped[float] = mapped_column(nullable=True)
    area_longitude: Mapped[float] = mapped_column(nullable=True)
    desc: Mapped[str] = mapped_column(nullable=True)
    protection: Mapped[str] = mapped_column(nullable=True)
    num_votes: Mapped[int] = mapped_column(nullable=True)

### For GaiaGPS data importing ###

class Trail(Base):
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

### FUNCTIONS ###

def get_engine():
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'password')
    db_host = os.getenv('DB_HOST', 'climb_wise-db-1')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'climb_wise_local')
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(db_url)

def get_sessionmaker(engine):
    from sqlalchemy.orm import sessionmaker
    return sessionmaker(bind=engine)

def get_conn():
    engine = get_engine()
    Session = get_sessionmaker(engine)
    return engine, Session
