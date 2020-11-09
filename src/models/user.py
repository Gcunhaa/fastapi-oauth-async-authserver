from .base import Base, db
from sqlalchemy_utils import PasswordType, EmailType, force_auto_coercion

force_auto_coercion()


class User(Base):
    __tablename__ = "users"

    fullname = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(
        PasswordType(schemes=["pbkdf2_sha512"]), nullable=False, unique=False
    )
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False, nullable=False)
