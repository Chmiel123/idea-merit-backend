import datetime
import string
import random
from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import TEXT
import bcrypt
from config.config import config
from model.postgres_serializer import PostgresSerializerMixin
from model.db import db
from model.profile.account_email import AccountEmail

class EmailVerification(db.Base, PostgresSerializerMixin):
    __tablename__ = 'email_verification'
    __table_args__ = {'schema': 'profile'}

    email = Column(TEXT, ForeignKey('profile.account_email.email', ondelete='CASCADE'), primary_key=True, unique=True, nullable=False)
    verification = Column(TEXT, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    

    @staticmethod
    def generate_verification(account_email: AccountEmail):
        db.session.query(EmailVerification).filter_by(email = account_email.email).delete()
        
        random_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(20))
        ev = EmailVerification(
            email=account_email.email,
            verification = random_string,
        )
        ev.save_to_db()
        return ev
        

    @staticmethod
    def verify(email: str, verification_key: str):
        found = EmailVerification.find_by_email(email)
        return found and found.verification == verification_key

    @staticmethod
    def find_by_email(email):
        return db.session.query(EmailVerification).filter_by(email = email).first()