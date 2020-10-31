import datetime
import string
import random
from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import TEXT
from model.postgres_serializer import PostgresSerializerMixin
from model.db import db
from model.profile.account_email import AccountEmail

class EmailVerification(db.Base, PostgresSerializerMixin):
    __tablename__ = 'email_verification'
    __table_args__ = {'schema': 'profile'}

    email = Column(TEXT, ForeignKey('profile.account_email.email', ondelete='CASCADE'), primary_key=True, unique=True, nullable=False)
    verification_key = Column(TEXT, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, email):
        self.email = email
        self.verification_key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(20))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def find_by_verify_key(verification_key: str):
        return db.session.query(EmailVerification).filter_by(verification_key = verification_key).first()

    @staticmethod
    def find_by_email(email):
        return db.session.query(EmailVerification).filter_by(email = email).first()

    @staticmethod
    def delete_by_email(email):
        return db.session.query(EmailVerification).filter_by(email = email).delete()