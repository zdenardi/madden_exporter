from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import (
    sessionmaker,
)

from models.helper_classes import Base

DATABASE_URL = "postgresql+psycopg://" "madden:madden@localhost:5432/madden"

engine = create_engine(
    DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def setup_db(engine: Engine):
    Base.metadata.create_all(engine)
