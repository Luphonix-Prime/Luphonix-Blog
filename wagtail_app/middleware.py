from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            needs_completion = request.session.get('needs_profile_completion', False)
            if needs_completion:
                profile_url = reverse('blog:profile_completion')
                if request.path != profile_url and not request.path.startswith('/admin/'):
                    return redirect(profile_url)
        
        response = self.get_response(request)
        return response