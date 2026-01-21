from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.deprecation import MiddlewareMixin


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