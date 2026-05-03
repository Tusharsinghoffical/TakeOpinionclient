from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin
from accounts.models import UserProfile


class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware that allows access to all pages without authentication.
    Login is still required for certain protected actions/features.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Allow access to all pages for all users
        # Authentication is handled at the view level for protected actions
        return None


class AutoPatientLoginMiddleware(MiddlewareMixin):
    """
    Disabled - website is fully public, no auto-login needed.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request):
        response = self.get_response(request)
        return response
