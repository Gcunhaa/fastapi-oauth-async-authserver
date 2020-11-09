from main import db

from datetime import datetime

from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy_utils import EmailType, generic_repr


db.JSONB, db.UUID, db.EmailType = (JSONB, UUID, EmailType)


@generic_repr
class Base(db.Model):
    __abstract__ = True

    created = db.Column(
        db.DateTime, default=datetime.utcnow, server_default=db.func.now()
    )

    last_updated = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=db.func.now(),
    )

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
