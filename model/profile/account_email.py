from sqlalchemy import Column, ForeignKey, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID, TEXT
import bcrypt
from config.config import config
from model.postgres_serializer import PostgresSerializerMixin
from model.db import db

class AccountEmail(db.Base, PostgresSerializerMixin):
    __tablename__ = 'account_email'
    __table_args__ = {'schema': 'profile'}

    
    account_id = Column(UUID(as_uuid=True), ForeignKey('profile.account.id', ondelete='CASCADE'), unique=False, nullable=False)
    email = Column(TEXT, primary_key=True, nullable=False, unique=True)
    verified = Column(BOOLEAN, nullable=False, default=False)
    primary = Column(BOOLEAN, nullable=False, default=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def find_by_email(email):
        return db.session.query(AccountEmail).filter_by(email = email).first()

    @staticmethod
    def delete_by_email(email):
        return db.session.query(AccountEmail).filter_by(email = email).delete()
