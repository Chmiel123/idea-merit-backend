from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.config import Config

db = None

class DB:
    def __init__(self, config: Config):
        self.connection_string = config.cfg["database"]
        self.engine = create_engine(self.connection_string)
        self.Base = declarative_base()
        self.metadata = self.Base.metadata
        self.metadata.bind = self.engine
        self.Session = sessionmaker(bind=self.engine, autoflush=True)
        self.session = self.Session()
        global db
        db = self
