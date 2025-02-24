from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Tick(Base):
    '''
    Represents a route that has been ticked. all raw ticks of the same route have been combined into
    a single Route row, with the "attempts" field to capture how many ticks that route has.
    Note this is different than how MP and OB store tickes.

    source: OB, MP, etc.
    '''
    __tablename__ = 'ticks'

    route_id: Mapped[int] = mapped_column(primary_key=True)
    route_name: Mapped[str] # not strictly necessary, but perhpas useful
    date: Mapped[str] = mapped_column(nullable=True)
    # your_stars: Mapped[float] = mapped_column(nullable=True)
    style: Mapped[str] = mapped_column(nullable=True)
    lead_style: Mapped[str] = mapped_column(nullable=True)
    attempts: Mapped[int] = mapped_column(nullable=True)
    source: Mapped[str] = mapped_column(nullable=True)
