from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, TEXT
import bcrypt
from model.postgres_serializer import PostgresSerializerMixin
from model.db import db
from model.profile import account

class LoginDirect(db.Base, PostgresSerializerMixin):
    __tablename__ = 'login_direct'
    __table_args__ = {'schema': 'profile'}

    account_id = Column(UUID(as_uuid=True), ForeignKey('profile.account.id', ondelete='CASCADE'), primary_key=True, unique=True, nullable=False)
    password = Column(TEXT, nullable=False)

    # account = relationship('Account', backref = 'direct_logins')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def generate_hash(password):
        #TODO: change rounds to config
        salt = bcrypt.gensalt(rounds=8)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_hash(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
