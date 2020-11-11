import uuid
import enum
import datetime
from sqlalchemy import Column, ForeignKey, INT, FLOAT, DateTime
from sqlalchemy.dialects.postgresql import UUID, ENUM
from model.postgres_serializer import PostgresSerializerMixin
from model.db import db
from model.profile import account

class VoteEventType(enum.Enum):
    positive = 1
    negative = 2

class VoteEvent(db.Base, PostgresSerializerMixin):
    __tablename__ = 'vote_event'
    __table_args__ = {'schema': 'event'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    event_type = Column(ENUM(VoteEventType), nullable=False)
    origin_id = Column(UUID(as_uuid=True), ForeignKey('profile.account.id', ondelete='CASCADE'), unique=False, nullable=False, index=True)
    target_id = Column(UUID(as_uuid=True), unique=False, nullable=False, index=True)
    value = Column(FLOAT, default=0.0)

    def __init__(self, event_type: VoteEventType, origin_id: uuid, target_id: uuid, value: float):
        self.event_type = event_type
        self.origin_id = origin_id
        self.target_id = target_id
        self.value = value

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def find_by_origin_id(origin_id, page=0, pagesize=10):
        return db.session.query(VoteEvent).filter_by(origin_id = origin_id).order_by(VoteEvent.created_date.desc()).limit(pagesize).offset(pagesize * page).all()
    
    @staticmethod
    def find_by_target_id(target_id, page=0, pagesize=10):
        return db.session.query(VoteEvent).filter_by(target_id = target_id).order_by(VoteEvent.created_date.desc()).limit(pagesize).offset(pagesize * page).all()
