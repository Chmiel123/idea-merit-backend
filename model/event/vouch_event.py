import uuid
import enum
import datetime
from sqlalchemy import Column, ForeignKey, INT, DateTime
from sqlalchemy.dialects.postgresql import UUID, ENUM
from model.postgres_serializer import PostgresSerializerMixin
from model.db import db
from model.profile import account

class VouchEventType(enum.Enum):
    start = 1
    stop = 2

class VouchEvent(db.Base, PostgresSerializerMixin):
    __tablename__ = 'vouch_event'
    __table_args__ = {'schema': 'event'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    event_type = Column(ENUM(VouchEventType), nullable=False)
    origin_id = Column(UUID(as_uuid=True), ForeignKey('profile.account.id', ondelete='CASCADE'), unique=False, nullable=False, index=True)
    top_id = Column(UUID(as_uuid=True), ForeignKey('profile.account.id', ondelete='CASCADE'), unique=False, nullable=False, index=True)
    bottom_id = Column(UUID(as_uuid=True), ForeignKey('profile.account.id', ondelete='CASCADE'), unique=False, nullable=False, index=True)

    def __init__(self, event_type: VouchEventType, origin_id: uuid, top_id: uuid, bottom_id: uuid):
        self.event_type = event_type
        self.origin_id = origin_id
        self.top_id = top_id
        self.bottom_id = bottom_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def find_by_ids(top_id, bottom_id, page=0, pagesize=10):
        return db.session.query(VouchEvent).filter_by(top_id = top_id, bottom_id = bottom_id).order_by(VouchEvent.created_date.desc()).limit(pagesize).offset(pagesize * page).all()

    @staticmethod
    def find_by_top_id(top_id, page=0, pagesize=10):
        return db.session.query(VouchEvent).filter_by(top_id = top_id).order_by(VouchEvent.created_date.desc()).limit(pagesize).offset(pagesize * page).all()

    @staticmethod
    def find_by_bottom_id(bottom_id, page=0, pagesize=10):
        return db.session.query(VouchEvent).filter_by(bottom_id = bottom_id).order_by(VouchEvent.created_date.desc()).limit(pagesize).offset(pagesize * page).all()
