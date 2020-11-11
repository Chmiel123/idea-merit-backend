import uuid
import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID, TEXT
from model.postgres_serializer import PostgresSerializerMixin
from model.db import db

class Idea(db.Base, PostgresSerializerMixin):
    __tablename__ = 'idea'
    __table_args__ = {'schema': 'system'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    parent_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    author_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    name = Column(TEXT, nullable=False, unique=True, index=True)
    content = Column(TEXT, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_of_life = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, parent_id: uuid, author_id: uuid, name: str, content: str):
        self.parent_id = parent_id
        self.author_id = author_id
        self.name = name
        self.content = content
        self.created_date = datetime.datetime.utcnow()
        self.end_of_life = datetime.datetime.utcnow()

    def add_resource(self, amount: float):
        self.end_of_life = self.end_of_life + datetime.timedelta(hours=amount)
        self.save_to_db()

    def remaining_life(self) -> float:
        return (self.end_of_life - datetime.datetime.utcnow()).total_seconds() / 60 / 60

    def is_root(self) -> bool:
        return self.parent_id is None

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def find_by_id(id):
        return db.session.query(Idea).filter_by(id = id).first()

    @staticmethod
    def find_by_name(name):
        return db.session.query(Idea).filter_by(name = name).first()

    @staticmethod
    def find_by_author_id(author_id, page=0, pagesize=10):
        return db.session.query(Idea).filter_by(author_id = author_id).order_by(Idea.created_date.desc()).limit(pagesize).offset(pagesize * page).all()

    @staticmethod
    def find_by_parent_id(parent_id, page=0, pagesize=10):
        return db.session.query(Idea).filter_by(parent_id = parent_id).order_by(Idea.created_date.desc()).limit(pagesize).offset(pagesize * page).all()
