from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from .models import BlogPage

def tag_view(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = BlogPage.objects.live().filter(tags=tag)
    return render(request, 'blog/tag_page.html', {
        'tag': tag,
        'posts': posts,
    })