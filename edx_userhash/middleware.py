from django.templatetags.static import static


class InjectUserHashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_authenticated:
            return response

        if (
            hasattr(request.user, 'userhash') and
            hasattr(response, 'content') and
            b'</head>' in response.content and
            'text/html' in response.get('Content-Type', '')
        ):
            user_hash = request.user.userhash.hash
            script = f"""
                <script>window.USER_HASH = "{user_hash}";</script>
                <script src="{static("edx_userhash/js/userhash_overlay.js")}"></script>
                <link rel="stylesheet" href="{static("edx_userhash/css/userhash_overlay.css")}" media="all">
            """
            response.content = response.content.replace(
                b'</head>', script.encode('utf-8') + b'</head>'
            )
        return response
