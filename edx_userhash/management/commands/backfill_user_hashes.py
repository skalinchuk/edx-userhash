from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from edx_userhash.models import UserHash
from edx_userhash.utils import generate_unique_hash

class Command(BaseCommand):
    help = "Generate hashes for legacy users"

    def handle(self, *args, **opts):
        User = get_user_model()
        missing = User.objects.filter(userhash__isnull=True)
        for user in missing.all():
            UserHash.objects.create(user=user, hash=generate_unique_hash(user.pk, user.get_username()))
        self.stdout.write(self.style.SUCCESS(f"Back-filled {missing.count()} users"))
