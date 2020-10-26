import uuid
import datetime
from sqlalchemy import Column, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, TEXT
from model.postgres_serializer import PostgresSerializerMixin
from model.db import db
from model.profile import login_direct, account_email

class Account(db.Base, PostgresSerializerMixin):
    __tablename__ = 'account'
    __table_args__ = {'schema': 'profile'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(TEXT, nullable=False, unique=True)
    domain = Column(TEXT, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    login_direct = relationship('LoginDirect', uselist=False, backref = 'account')
    emails = relationship('AccountEmail', backref = 'account')
    
    UniqueConstraint('name', 'domain')

    def __init__(self, username):
        self.name = username

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def find_by_id(id):
        return db.session.query(Account).filter_by(id = id).first()

    @staticmethod
    def find_by_username(username, domain=None):
        return db.session.query(Account).filter_by(name = username, domain=domain).first()
    