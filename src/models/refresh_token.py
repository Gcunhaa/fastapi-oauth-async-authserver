from .base import db
from sqlalchemy_utils import force_auto_coercion, IPAddressType
from datetime import datetime, timedelta

force_auto_coercion()


class RefreshToken(db.Model):
    __tablename__ = "refresh_tokens"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    valid_until = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.String(32), unique=False, nullable=False)
