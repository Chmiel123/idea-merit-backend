import uuid
from sqlalchemy import Column, ForeignKey, BOOLEAN, INT
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from model.postgres_serializer import PostgresSerializerMixin
from model.db import db
from model.profile import account

class VouchRequest(db.Base, PostgresSerializerMixin):
    __tablename__ = 'vouch_request'
    __table_args__ = {'schema': 'profile'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    top_id = Column(UUID(as_uuid=True), ForeignKey('profile.account.id', ondelete='CASCADE'), unique=False, nullable=False)
    bottom_id = Column(UUID(as_uuid=True), ForeignKey('profile.account.id', ondelete='CASCADE'), unique=False, nullable=False)
    top_accept = Column(BOOLEAN, nullable=False, default=False)
    bottom_accept = Column(BOOLEAN, nullable=False, default=False)

    def __init__(self, top_id: uuid, bottom_id: uuid):
        self.top_id = top_id
        self.bottom_id = bottom_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def find_by_ids(top_id, bottom_id):
        return db.session.query(VouchRequest).filter_by(top_id = top_id, bottom_id = bottom_id).first()

    @staticmethod
    def find_by_top_id(top_id):
        return db.session.query(VouchRequest).filter_by(top_id = top_id).all()

    @staticmethod
    def find_by_bottom_id(bottom_id):
        return db.session.query(VouchRequest).filter_by(bottom_id = bottom_id).all()

    @staticmethod
    def delete_by_ids(top_id, bottom_id):
        db.session.query(VouchRequest).filter_by(top_id = top_id, bottom_id = bottom_id).delete()