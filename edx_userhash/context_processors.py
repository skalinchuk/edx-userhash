def user_hash(request):
    """
    Injects USER_HASH into every template render.
    Safe for anonymous users.
    """
    if (
        request.user.is_authenticated
        and hasattr(request.user, "userhash")
    ):
        return {"USER_HASH": request.user.userhash.hash}
    return {}
