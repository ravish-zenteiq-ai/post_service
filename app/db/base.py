from sqlalchemy.orm import Session
import fastapi
from sqlalchemy.dialects import postgresql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



DB_URL = 'postgresql+psycopg://postgres:root1204@localhost/fastapi'


engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine, autoflush= False, autocommit=False)

Base = declarative_base()