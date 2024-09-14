from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Configuration

engine = create_engine(f"sqlite:///{Configuration.db_path}")
session = sessionmaker(bind=engine)()

