from sqlalchemy import Column, String
from model.db import db
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

class Person(db.Base):
    __tablename__ = 'person'
    __table_args__ = {'schema': 'personal'}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(250), nullable=False)