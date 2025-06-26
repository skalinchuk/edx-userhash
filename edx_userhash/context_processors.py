def userhash_context(request):
    if request.user.is_authenticated and hasattr(request.user, 'userhash'):
        return {"USER_HASH": request.user.userhash.hash}
    return {}
