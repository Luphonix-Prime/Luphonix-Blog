from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('tag/<str:tag_slug>/', views.tag_view, name='tag'),
]