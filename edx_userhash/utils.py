import hashlib
import hmac
import secrets
from django.conf import settings

from edx_userhash.models import UserHash


def generate_unique_hash(user_pk: int, username: str) -> str:
    result = None
    attempts = 0
    hash_length = min(UserHash._meta.get_field('hash').max_length, 64)
    while result is None or UserHash.objects.filter(hash=result).exists():
        if attempts > 10:
            raise Exception("Can not generate unique hash. Too many attempts")
        salt = secrets.token_hex(8)
        msg = f"{user_pk}:{username}:{salt}".encode()
        result = hmac.new(settings.SECRET_KEY.encode(), msg, hashlib.sha256).hexdigest()[:hash_length]
        attempts += 1
    return result
