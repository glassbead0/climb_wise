import os
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()

class Base(DeclarativeBase):
    pass

def get_engine(db_name):
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_host = os.getenv('POSTGRES_HOST', 'climb_wise-db-1')
    db_port = os.getenv('POSTGRES_PORT', 5432)
    db_name = db_name
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(db_url)

def get_sessionmaker(engine):
    return sessionmaker(bind=engine)

def get_conn(db_name=os.getenv('POSTGRES_NAME', 'climb_wise_local_v2')):
    """
    Returns a connection to the database

    Args:
        db_name (str): The name of the database to connect to
    """
    engine = get_engine(db_name)
    Session = get_sessionmaker(engine)
    return engine, Session
