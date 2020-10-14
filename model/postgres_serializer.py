import uuid
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.dialects.postgresql import TEXT

class PostgresSerializerMixin(SerializerMixin):
    serialize_types = (
        (uuid.UUID, str),
        (TEXT, str)
    )