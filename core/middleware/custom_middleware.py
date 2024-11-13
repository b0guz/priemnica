from django.http import Http404
import re


class AdminPagesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        if request.path.startswith('/admin') and not request.user.is_superuser:
            raise Http404()
        """

        regex_list = [
            r"^/admin",
            r"^/import",
            r"^/disnotes/\d*/remove",
        ]
        for pattern in regex_list:
            if re.match(pattern, request.path) and not request.user.is_superuser:
                raise Http404()

        return self.get_response(request)
