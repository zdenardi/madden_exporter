from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from models.helper_classes import Base


class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[str]
    season: Mapped[int]
    week: Mapped[int]
    payload: Mapped[dict] = mapped_column(JSON)
