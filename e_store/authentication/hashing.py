from datetime import datetime

from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_ctx.verify(plain_password, hashed_password)


def create_ctx_token(password: str, context_string: str, current_time: datetime) -> str:
    """
    Create a unique token for each user used in something like email verification.

    :param password: The user's password.
    :param context_string: An arbitrary string that may resemble the context you want
        to use the user token in.
    :param current_time: The current datetime.
    :return: A unique token string.

    e.g.::

        # for email verification
        user = User(**kwargs)
        token = user.user_ctx_token('email verification')
    """
    return f"""{context_string}{password[-6:]}{current_time.strftime("%m%d%Y%H%M%S")}""".strip()
