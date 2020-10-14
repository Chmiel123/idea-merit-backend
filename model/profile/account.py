import uuid
import datetime
from sqlalchemy import Column, UniqueConstraint, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, TEXT
import bcrypt
from model.postgres_serializer import PostgresSerializerMixin
from model.db import db
from model.profile import login_direct

class Account(db.Base, PostgresSerializerMixin):
    __tablename__ = 'account'
    __table_args__ = {'schema': 'profile'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(TEXT, nullable=False, unique=True)
    domain = Column(TEXT, nullable=True)
    registered_date = Column(DateTime, default=datetime.datetime.utcnow)

    direct_login = relationship('LoginDirect', uselist=False, backref = 'account')

    UniqueConstraint('name', 'domain')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def find_by_username(username, domain=None):
        return db.session.query(Account).filter_by(name = username, domain=domain).first()
    