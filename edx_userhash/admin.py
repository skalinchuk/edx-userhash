from django.contrib import admin
from django.utils.html import format_html
from .models import UserHash


@admin.register(UserHash)
class UserHashAdmin(admin.ModelAdmin):
    """Read-only view of the one-to-one hash attached to each user."""

    # Columns that appear in the changelist
    list_display = ("user_link", "hash", "created")
    list_select_related = ("user",)
    search_fields = ("user__username", "user__email", "hash")
    list_filter = ("created",)

    # Disallow edits in the admin UI
    readonly_fields = ("user", "hash", "created")
    actions = None

    # Remove the “Add” and “Delete” buttons
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # Helper to link directly to the User object
    @admin.display(description="User", ordering="user__username")
    def user_link(self, obj):
        url = f"/admin/auth/user/{obj.user.pk}/change/"
        return format_html('<a href="{}">{}</a>', url, obj.user.get_username())
