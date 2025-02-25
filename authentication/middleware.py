from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated and request.user.is_verified:
            # Check if profile is incomplete (e.g., missing first_name)
            if not request.user.first_name:
                if request.path not in [reverse('complete_profile'), reverse('logout')]:
                    return redirect('complete_profile')
        
        return response