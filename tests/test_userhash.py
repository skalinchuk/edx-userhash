"""
Unit-tests for the edx-userhash plugin.

Run with:
    pytest -q
"""

import re
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.contrib.admin.sites import AdminSite
from django.core.management import call_command
from django.test.client import RequestFactory

from edx_userhash.models import UserHash
from edx_userhash.utils import generate_unique_hash
from edx_userhash.admin import UserHashAdmin


# ---------------------------------------------------------------------------
# utils.generate_unique_hash
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_generate_unique_hash_format_and_uniqueness():
    """Hash must be 64 hex chars and different on repeated calls."""
    h1 = generate_unique_hash(42)
    h2 = generate_unique_hash(42)

    assert len(h1) == 64
    assert re.fullmatch(r"[0-9a-f]{64}", h1)
    assert h1 != h2


# ---------------------------------------------------------------------------
# UserHash model tests
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_userhash_str_representation():
    """`str(instance)` should match '<UserHash, User ID: {pk}>'."""
    User = get_user_model()
    user = User.objects.create_user(username="henry", password="x")
    uh: UserHash = user.userhash

    assert str(uh) == f"<UserHash, User ID: {user.pk}>"


@pytest.mark.django_db
def test_signal_creates_one_hash_per_new_user():
    """Creating a user should leave exactly one related UserHash row."""
    User = get_user_model()
    alice = User.objects.create_user(username="alice", password="x")

    assert hasattr(alice, "userhash")
    assert UserHash.objects.filter(user=alice).count() == 1


# ---------------------------------------------------------------------------
# management command: backfill_user_hashes
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_backfill_command_creates_missing_hash_and_is_idempotent():
    User = get_user_model()

    # Legacy user with no hash
    bob = User.objects.create_user(username="bob", password="x")
    UserHash.objects.filter(user=bob).delete()
    bob.refresh_from_db()
    assert not hasattr(bob, "userhash")

    # Normal user that already has a hash
    carol = User.objects.create_user(username="carol", password="x")
    carols_hash = carol.userhash.hash

    # first run should create exactly one missing hash
    call_command("backfill_user_hashes")
    bob.refresh_from_db()
    carol.refresh_from_db()

    assert hasattr(bob, "userhash")
    assert carols_hash == carol.userhash.hash
    total_after_first = UserHash.objects.count()

    # second run must be a no-op (idempotent)
    bobs_hash = bob.userhash.hash
    call_command("backfill_user_hashes")
    bob.refresh_from_db()
    carol.refresh_from_db()
    assert UserHash.objects.count() == total_after_first
    assert carols_hash == carol.userhash.hash
    assert carols_hash == carol.userhash.hash


@pytest.mark.django_db
def test_login_signal_backfills_missing_hash():
    """Logging in without a hash should trigger creation of exactly one hash."""
    User = get_user_model()
    rf = RequestFactory()

    # Legacy user: remove the hash the post-save signal would have added
    frank = User.objects.create_user(username="frank", password="x")
    UserHash.objects.filter(user=frank).delete()
    frank.refresh_from_db()
    assert not hasattr(frank, "userhash")

    # Fire the login signal manually
    request = rf.get("/")
    user_logged_in.send(sender=User, request=request, user=frank)

    frank.refresh_from_db()
    assert hasattr(frank, "userhash")
    assert UserHash.objects.filter(user=frank).count() == 1


@pytest.mark.django_db
def test_login_signal_is_idempotent_when_hash_exists():
    """Logging in again must not create a second hash for the same user."""
    User = get_user_model()
    rf = RequestFactory()

    grace = User.objects.create_user(username="grace", password="x")
    initial_hash_pk = grace.userhash.pk
    initial_count = UserHash.objects.count()

    # Trigger login signal; hash already exists
    user_logged_in.send(sender=User, request=rf.get("/"), user=grace)

    assert UserHash.objects.count() == initial_count
    grace.refresh_from_db()
    assert grace.userhash.pk == initial_hash_pk

# ---------------------------------------------------------------------------
# admin class behaviour
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_admin_is_read_only():
    """The custom ModelAdmin must not allow add/delete operations."""
    site = AdminSite()
    admin = UserHashAdmin(UserHash, site)

    assert admin.has_add_permission(request=None) is False
    assert admin.has_delete_permission(request=None, obj=None) is False
