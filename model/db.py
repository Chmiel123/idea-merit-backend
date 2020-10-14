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
    
    def drop_all(self):
        cnn = self.engine.raw_connection()
        cur = cnn.cursor()
        cur.execute("""
            select s.nspname as s, t.relname as t
            from pg_class t join pg_namespace s on s.oid = t.relnamespace
            where t.relkind = 'r'
            and s.nspname !~ '^pg_' and s.nspname != 'information_schema'
            order by 1,2
            """)
        tables = cur.fetchall()  # make sure they are the right ones

        for t in tables:
            cur.execute(f"drop table if exists {t[0]}.{t[1]} cascade")

        cnn.commit()  # goodbye
