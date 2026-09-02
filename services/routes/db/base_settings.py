from sqlalchemy import create_engine
import os

engine = create_engine(os.getenv("DB_URL"), echo=True)