from datetime import timedelta
import time
import jwt
from passlib.context import CryptContext
from .config import settings

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain, hashed):
    return pwd.verify(plain, hashed)


def hash_password(plain):
    return pwd.hash(plain)


def create_access_token(subject: dict, expires_seconds: int = None):
    # Use POSIX time (time.time()) as the canonical clock reference so iat/exp
    # align with the jwt library's validation which uses time.time(). This
    # avoids subtle timezone/naive-datetime mismatches on some platforms.
    now_ts = int(time.time())
    exp_seconds = expires_seconds or settings.JWT_EXP_SECONDS
    exp_ts = now_ts + int(exp_seconds)
    payload = {"sub": subject, "iat": now_ts, "exp": exp_ts}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_token(token: str):
    # Use configured leeway to tolerate small clock skew (in seconds).
    leeway = getattr(settings, 'JWT_LEEWAY_SECONDS', 0)
    # Rely only on configurable leeway for clock skew. Do NOT fallback to
    # skipping 'iat' verification — that would reduce security. If you need
    # to allow larger skew in development, increase JWT_LEEWAY_SECONDS in
    # your .env or Settings.
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM], leeway=leeway)