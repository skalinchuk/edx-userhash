import hashlib
import hmac
import secrets
from django.conf import settings


def generate_unique_hash(user_pk: int) -> str:
    salt = secrets.token_hex(8)
    msg = f"{user_pk}:{salt}".encode()
    return hmac.new(settings.SECRET_KEY.encode(), msg, hashlib.sha256).hexdigest()
