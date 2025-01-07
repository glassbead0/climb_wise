from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import insert


Base = declarative_base()

class Tick(Base):
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
    

class Route(Base):
    '''
    Represents a route that has been ticked. the difference between this and the Tick table
    is that all ticks of the same route have been combined into a single Route row, with
    the "attempts" field to capture how many ticks that route has.
    '''
    __tablename__ = 'routes'

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

def get_engine():
    db_url = "postgresql://postgres:password@climb_wise-db-1:5432/climb_wise_local"
    return create_engine(db_url)

def get_sessionmaker(engine):
    from sqlalchemy.orm import sessionmaker
    return sessionmaker(bind=engine)
