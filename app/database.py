from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import DATABASE_URL

Base = declarative_base()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    with SessionLocal() as session:
        yield session


def init_db():
    Base.metadata.create_all(bind=engine)


def close_db():
    engine.dispose()
