import os

from sqlalchemy import create_engine

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])

Session = scoped_session(sessionmaker(bind=engine))
