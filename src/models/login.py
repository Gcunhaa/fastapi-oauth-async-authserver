from .base import db
from sqlalchemy_utils import force_auto_coercion, IPAddressType
from datetime import datetime

force_auto_coercion()


class LoginLog(db.Model):
    __tablename__ = "login_logs"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    login_date = db.Column(
        db.DateTime, default=datetime.utcnow, server_default=db.func.now()
    )

    grant_type = db.Column(
        db.String(50), unique=False, nullable=False, default="password"
    )
    ip_address = db.Column(IPAddressType, nullable=False, unique=False)
