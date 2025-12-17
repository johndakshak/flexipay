from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB_HOST=os.getenv('DB_HOST')
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_DATABASE=os.getenv('DB_DATABASE')
DB_PORT=os.getenv('DB_PORT')

SQLALCHEMY_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'

engine = create_engine(SQLALCHEMY_URL, echo=True)

Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = Session()
    
    try:
        yield db
    finally:
        db.close()