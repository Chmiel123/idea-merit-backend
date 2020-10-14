import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from model.db import db
from model.personal.person import Person

class Address(db.Base):
    __tablename__ = 'address'
    __table_args__ = {'schema': 'personal'}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    street_name = Column(String(250))
    street_name_2 = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(UUID(as_uuid=True), ForeignKey('personal.person.id'))
    person = relationship(Person)