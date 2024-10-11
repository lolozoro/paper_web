from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base

engine = create_engine('postgresql://postgres:difyai123456@127.0.0.1:5432/paper_db')

Base.metadata.create_all(engine)
