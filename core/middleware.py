from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware that requires authentication for all pages except:
    - Home page (landing page)
    - Login page
    - Signup page
    - Admin pages (handled by Django's built-in authentication)
    - Health check endpoints
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Allow access to admin URLs
        if request.path.startswith('/admin/'):
            return None
            
        # Allow access to static files check
        if request.path.startswith('/static-check/'):
            return None
            
        # Allow access to health check
        if request.path.startswith('/health/'):
            return None
            
        # Public URLs that don't require authentication
        public_urls = [
            '/',  # Home page
            '/accounts/login/',
            '/accounts/signup/',
            '/accounts/logout/',  # Logout should be accessible to redirect properly
        ]
        
        # Check if the current path is a public URL
        if request.path in public_urls:
            return None
            
        # If user is authenticated, allow access
        if request.user.is_authenticated:
            return None
            
        # For all other URLs, redirect to login
        return redirect('login')