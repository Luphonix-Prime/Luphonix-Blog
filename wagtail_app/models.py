# Add this import at the top if not already present
from taggit.models import Tag

# Inside your BlogIndexPage class, add or modify the get_context method
def get_context(self, request, *args, **kwargs):
    context = super().get_context(request, *args, **kwargs)
    
    # Get all tags from all blog posts
    all_tags = Tag.objects.all()
    
    # Add to context
    context['all_tags'] = all_tags
    
    return context