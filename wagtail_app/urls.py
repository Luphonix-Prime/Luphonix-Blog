from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import redirect
from django.urls import reverse

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images.views.serve import ServeView

from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import search

# Custom middleware to handle admin login redirect
def admin_login_redirect(request):
    if not request.user.is_authenticated:
        print("User is not authenticated, redirecting to login.")
        return redirect('blog:login')
    # Check if user has Wagtail admin access
    if request.user.has_perm('wagtailadmin.access_admin'):
        print("User is authenticated and has wagtailadmin access, redirecting to wagtailadmin_home.")
        return redirect('wagtailadmin_home')
    else:
        print("User is authenticated but does NOT have wagtailadmin access, redirecting to homepage.")
        # Optionally, show a message or redirect elsewhere
        return redirect('wagtail_serve', '')

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('django-admin/', admin.site.urls),
    path('admin/login/', admin_login_redirect),  # Add custom redirect for admin login
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    
    # Include blog URLs
    path('blog/', include('wagtail_app.blog.urls')),
    path('search/', search, name='search'),
    
    # Serve Wagtail images
    path('images/<str:signature>/<str:image_id>/<str:filter_spec>/<str:filename>', 
         ServeView.as_view(), 
         name='wagtailimages_serve'),
    
    # Wagtail URLs should be last
    path('', include(wagtail_urls)),
    
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)