from django.conf import settings
from django.urls import path, include
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images.views.serve import ServeView

from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    
    # Include blog URLs
    path('blog/', include('wagtail_app.blog.urls')),
    
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