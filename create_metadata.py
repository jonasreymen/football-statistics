import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

from app.models.models import Base

load_dotenv(override=True)

engine = create_engine(os.getenv("DATABASE_CONNECTION"))

Base.metadata.create_all(bind=engine)