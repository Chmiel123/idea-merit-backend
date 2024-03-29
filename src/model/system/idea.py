import uuid
import datetime
from sqlalchemy import Column, UniqueConstraint, DateTime, FLOAT, INT
from sqlalchemy.dialects.postgresql import UUID, TEXT
from model.postgres_serializer import PostgresSerializerMixin
from model.db import db

class Idea(db.Base, PostgresSerializerMixin):
    __tablename__ = 'idea'
    __table_args__ = {'schema': 'system'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    parent_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    author_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    name = Column(TEXT, nullable=False, index=True)
    content = Column(TEXT, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_of_life = Column(DateTime, default=datetime.datetime.utcnow)

    total_life_direct = Column(FLOAT)
    total_life_inherited = Column(FLOAT)

    total_children = Column(INT)

    UniqueConstraint('name', 'parent_id')

    def __init__(self, parent_id: uuid, author_id: uuid, name: str, content: str):
        self.parent_id = parent_id
        self.author_id = author_id
        self.name = name
        self.content = content
        self.created_date = datetime.datetime.utcnow()
        self.end_of_life = datetime.datetime.utcnow()
        self.total_life_direct = 0.0
        self.total_life_inherited = 0.0
        self.total_children = 0

    def add_resource_direct(self, amount: float):
        self.end_of_life = self.end_of_life + datetime.timedelta(hours=amount)
        self.total_life_direct += amount
        self.save_to_db()

    def add_resource_inherited(self, amount: float):
        self.end_of_life = self.end_of_life + datetime.timedelta(hours=amount)
        self.total_life_inherited += amount
        self.save_to_db()

    def total_life(self) -> float:
        return self.total_life_direct + self.total_life_inherited

    def remaining_life(self) -> float:
        return (self.end_of_life - datetime.datetime.utcnow()).total_seconds() / 60 / 60

    def is_root(self) -> bool:
        return self.parent_id is None

    def is_dead(self) -> bool:
        if (self.is_root()):
            return False
        return self.remaining_life() < 0

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
    def find_by_name_and_parent(name, parent_id):
        return db.session.query(Idea).filter_by(name = name, parent_id = parent_id).first()

    @staticmethod
    def find_by_author_id(author_id, page=0, pagesize=10):
        return db.session.query(Idea).filter_by(author_id = author_id).order_by(Idea.created_date.desc()).limit(pagesize).offset(pagesize * page).all()

    @staticmethod
    def find_by_parent_id(parent_id, page=0, pagesize=10):
        return db.session.query(Idea).filter_by(parent_id = parent_id).order_by(Idea.created_date.desc()).limit(pagesize).offset(pagesize * page).all()
