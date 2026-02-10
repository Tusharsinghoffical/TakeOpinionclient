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
    Middleware that automatically logs in a default patient user
    if no user is currently authenticated.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request):
        # Check if user is not authenticated
        if not request.user.is_authenticated:
            try:
                # Try to get the default patient user
                # You can change this to any existing patient username
                default_patient_username = 'tusharsinghkumar02'  # Change this as needed
                user = User.objects.get(username=default_patient_username)

                # Verify this user has a patient profile
                if hasattr(user, 'userprofile') and user.userprofile.user_type == 'patient':
                    # Log in the user automatically
                    login(request, user)
                    print(f"Auto-logged in patient: {user.username}")

            except User.DoesNotExist:
                # If default patient doesn't exist, try to find any patient
                try:
                    patient_user = User.objects.filter(
                        userprofile__user_type='patient'
                    ).first()
                    if patient_user:
                        login(request, patient_user)
                        print(
                            f"Auto-logged in patient: {patient_user.username}")
                except:
                    pass
            except Exception as e:
                print(f"Auto-login failed: {e}")
                pass

        response = self.get_response(request)
        return response
