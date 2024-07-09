from django.conf import settings
from django.contrib.auth.views import LoginView


class LoginAndSetLang(LoginView):

    def get_language(self, user):
        # If the user already has set some preference, use it
        if user.preferred_locale in dict(settings.LANGUAGES):
            return user.preferred_locale
        # Use the node default preferred language
        node = user.get_node()
        if node is not None:
            return node.preferred_locale
        # Otherwise return default system language
        return settings.LANGUAGE_CODE

    def form_valid(self, form):
        response = super().form_valid(form)
        user_lang = self.get_language(form.get_user())

        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            user_lang,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
        return response
