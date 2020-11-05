from .base import db
from sqlalchemy_utils import force_auto_coercion, IPAddressType
from datetime import datetime, timedelta

force_auto_coercion()

class ConfirmEmailToken(db.Model):
    __tablename__ = "confirm_email_tokens"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    pre_user_id = db.Column(db.BigInteger, db.ForeignKey('pre_users.id'))
    valid_until = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.String(32), unique=False, nullable=False)
