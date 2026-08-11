from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from models.helper_classes import Base


class EATokenInfo(Base):
    __tablename__ = "ea_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    access_token: Mapped[str]
    refresh_token: Mapped[str]
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
