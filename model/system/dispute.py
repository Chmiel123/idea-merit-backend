import uuid
import enum
import datetime
from sqlalchemy import Column, DateTime, FLOAT
from sqlalchemy.dialects.postgresql import UUID, ENUM
from config.config import config
from model.postgres_serializer import PostgresSerializerMixin
from model.db import db

class DisputeResultType(enum.Enum):
    in_progress = 1
    stay = 2
    dead = 3

class Dispute(db.Base, PostgresSerializerMixin):
    __tablename__ = 'dispute'
    __table_args__ = {'schema': 'system'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    idea_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    author_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    votes_for = Column(FLOAT, default=0.0)
    votes_against = Column(FLOAT, default=0.0)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime, default=datetime.datetime.utcnow)
    result = Column(ENUM(DisputeResultType), nullable=False, default=DisputeResultType.in_progress)

    def __init__(self, idea_id: uuid, author_id: uuid):
        self.idea_id = idea_id
        self.author_id = author_id
        self.end_date = self.created_date + datetime.timedelta(days=config['limit']['dispute_duration_hours'])

    def vote_for(self, amount: float):
        self.votes_for += amount
        self.save_to_db()

    def vote_against(self, amount: float):
        self.votes_against += amount
        self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def find_by_idea_id(idea_id):
        return db.session.query(Dispute).filter_by(idea_id = idea_id).first()

    @staticmethod
    def find_by_author_id(author_id, page=0, pagesize=10):
        return db.session.query(Dispute).filter_by(author_id = author_id).limit(pagesize).offset(pagesize * page).all()