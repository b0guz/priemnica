from django.contrib.sessions.models import Session
from app_user.models import LoggedInUser


class OneSessionPerUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            session_key = request.session.session_key

            try:
                logged_in_user = request.user.logged_in_user
                stored_session_key = logged_in_user.session_key

                if stored_session_key != session_key:
                    Session.objects.filter(session_key=stored_session_key).delete()
                logged_in_user.session_key = session_key
                logged_in_user.save()
            except LoggedInUser.DoesNotExist:
                LoggedInUser.objects.create(user=request.user, session_key=session_key)

        response = self.get_response(request)

        return response
