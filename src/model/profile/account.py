import uuid
import datetime
from util.exception import ModelException
from sqlalchemy import Column, UniqueConstraint, DateTime, FLOAT
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, TEXT
from model.postgres_serializer import PostgresSerializerMixin
from model.db import db
from model.profile import account_password, account_email

class Account(db.Base, PostgresSerializerMixin):
    __tablename__ = 'account'
    __table_args__ = {'schema': 'profile'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(TEXT, nullable=False, index=True)
    domain = Column(TEXT, nullable=True, index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    virtual_resource_start_date = Column(DateTime, default=datetime.datetime.utcnow)
    virtual_resource_speed = Column(FLOAT, default=0.0)
    virtual_resource_accrued = Column(FLOAT, default=0.0)
    total_resource_spent = Column(FLOAT, default=0.0)

    account_password = relationship('AccountPassword', uselist=False, backref = 'account')
    emails = relationship('AccountEmail', backref = 'account')
    
    UniqueConstraint('name', 'domain')

    def __init__(self, username):
        self.name = username

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_total_resource(self) -> float:
        new_date = datetime.datetime.utcnow()
        hours_accrued = (new_date - self.virtual_resource_start_date).total_seconds() / 60 / 60 * self.virtual_resource_speed
        self.virtual_resource_accrued += hours_accrued
        self.virtual_resource_start_date = new_date
        self.save_to_db()
        return self.virtual_resource_accrued

    def get_total_resource(self) -> float:
        return self.update_total_resource()

    def set_resource_speed(self, new_speed: float):
        self.update_total_resource()
        self.virtual_resource_speed = new_speed
        self.save_to_db()

    def subtract_resource(self, amount: float) -> float:
        if amount > self.update_total_resource():
            return 0
        self.virtual_resource_accrued -= amount
        self.total_resource_spent += amount
        self.save_to_db()
        return amount

    @staticmethod
    def find_by_id(id: uuid):
        return db.session.query(Account).filter_by(id = id).first()

    @staticmethod
    def find_by_username(username, domain=None):
        return db.session.query(Account).filter_by(name = username, domain=domain).first()
    