import datetime
import string
import random
import uuid
from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import TEXT, UUID
from model.postgres_serializer import PostgresSerializerMixin
from model.db import db
from model.profile.account_email import AccountEmail

class PasswordReset(db.Base, PostgresSerializerMixin):
    __tablename__ = 'password_reset'
    __table_args__ = {'schema': 'profile'}

    account_id = Column(UUID(as_uuid=True), ForeignKey('profile.account.id', ondelete='CASCADE'), primary_key=True, unique=True, nullable=False)
    verification_key = Column(TEXT, nullable=False, index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, account_id: uuid):
        self.account_id = account_id
        self.verification_key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(20))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def find_by_verify_key(verification_key: str):
        return db.session.query(PasswordReset).filter_by(verification_key = verification_key).first()

    @staticmethod
    def find_by_account_id(account_id):
        return db.session.query(PasswordReset).filter_by(account_id = account_id).first()

    @staticmethod
    def delete_by_account_id(account_id):
        return db.session.query(PasswordReset).filter_by(account_id = account_id).delete()