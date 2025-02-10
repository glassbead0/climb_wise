# only run this once to create all database tables
from ..models.base import Base, get_conn
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database

def main():
  load_dotenv()
  engine, Session = get_conn()
  create_database(engine.url)
  Base.metadata.create_all(engine)

def create_database(engine_url):
  if not database_exists(engine_url):
    print("DB does not exist, creating... at ", engine_url)
    create_database(engine_url)

if __name__ == '__main__':
  main()