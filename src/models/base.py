import os
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()

class Base(DeclarativeBase):
    pass

def get_engine():
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST', 'climb_wise-db-1')
    db_port = os.getenv('DB_PORT', 5432)
    db_name = 'climb_wise_local_v2' # os.getenv('DB_NAME', 'climb_wise_local_v2')
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(db_url)

def get_sessionmaker(engine):
    return sessionmaker(bind=engine)

def get_conn():
    engine = get_engine()
    Session = get_sessionmaker(engine)
    return engine, Session
