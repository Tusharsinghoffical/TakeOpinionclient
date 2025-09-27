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
    - Doctors pages (publicly accessible)
    - Treatments pages (publicly accessible)
    - Hospitals pages (publicly accessible)
    - Blogs pages (publicly accessible)
    - Search page (publicly accessible)
    - API endpoints (publicly accessible)
    - Content API endpoint (publicly accessible)
    - Reviews page (publicly accessible)
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
            
        # Allow access to API endpoints
        if request.path.startswith('/api/') or request.path.startswith('/accounts/api/'):
            return None
            
        # Public URLs that don't require authentication
        public_urls = [
            '/',  # Home page
            '/accounts/login/',
            '/accounts/signup/',
            '/accounts/logout/',  # Logout should be accessible to redirect properly
            '/doctors/',  # Doctors list page
            '/treatments/',  # Treatments list page
            '/hospitals/',  # Hospitals list page
            '/blogs/',  # Blogs list page
            '/search/',  # Search page
            '/accounts/reviews/',  # Reviews page
            '/content/',  # Content API endpoint
        ]
        
        # Also allow access to individual doctor detail pages
        if request.path.startswith('/doctors/') and request.path.endswith('/'):
            return None
            
        # Also allow access to individual treatment detail pages
        if request.path.startswith('/treatments/') and request.path.endswith('/'):
            return None
            
        # Also allow access to individual hospital detail pages
        if request.path.startswith('/hospitals/') and request.path.endswith('/'):
            return None
            
        # Also allow access to individual blog detail pages
        if request.path.startswith('/blogs/') and request.path.endswith('/'):
            return None
            
        # Check if the current path is a public URL
        if request.path in public_urls:
            return None
            
        # If user is authenticated, allow access
        if request.user.is_authenticated:
            return None
            
        # For all other URLs, redirect to login
        return redirect('login')