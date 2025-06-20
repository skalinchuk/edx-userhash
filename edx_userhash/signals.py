from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model, models as auth_models
from django.contrib.auth.signals import user_logged_in
from .models import UserHash
from .utils import generate_unique_hash

User = get_user_model()


@receiver(post_save, sender=User, dispatch_uid="create_user_hash")
def create_user_hash(sender, instance: User, created, **kwargs):
    if created and not hasattr(instance, "userhash"):
        UserHash.objects.create(user=instance, hash=generate_unique_hash(instance.pk, instance.get_username()))


@receiver(user_logged_in, sender=User, dispatch_uid="verify_user_hash")
def verify_user_hash(sender, request, **kwargs):
    instance = kwargs.pop('user')
    if not hasattr(instance, "userhash"):
        UserHash.objects.create(user=instance, hash=generate_unique_hash(instance.pk, instance.get_username()))
