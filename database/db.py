from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Lighthouse DB configuration
SQLALCHEMY_LIGHTHOUSE_DATABASE_URL = os.getenv("LIGHTHOUSE_DATABASE_URL")
engine = create_engine(SQLALCHEMY_LIGHTHOUSE_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# reflect the tables
lighthouse_metadata = MetaData()
lighthouse_metadata.reflect(engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
