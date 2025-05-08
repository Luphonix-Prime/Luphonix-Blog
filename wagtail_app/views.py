from django.shortcuts import render, redirect
from wagtail.models import Page
from wagtail.search.backends import get_search_backend
from wagtail_app.blog.models import Author  # Update this line
from wagtail.images.models import Image  # Ensure this import is present
from django.contrib import messages

def search(request):
    search_query = request.GET.get('query', None)
    if search_query:
        search_backend = get_search_backend()
        # Add Page.objects.live() as the model_or_queryset parameter
        search_results = search_backend.search(search_query, Page.objects.live())
    else:
        search_results = []
    
    return render(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
def profile_completion(request):
    if request.method == 'POST':
        # Handle form submission
        bio = request.POST.get('bio', '')
        website = request.POST.get('website', '')
        twitter = request.POST.get('twitter', '')
        linkedin = request.POST.get('linkedin', '')
        photo = request.FILES.get('profile_picture', None)

        # Check if profile picture is required
        if not photo:
            messages.error(request, 'Profile picture is required')
            return render(request, 'profile_completion.html')

        # Get or create Author profile
        author, created = Author.objects.get_or_create(email=request.user.email)
        author.name = request.user.username
        author.bio = bio
        author.website = website
        author.twitter = twitter
        author.linkedin = linkedin
        
        try:
            if photo.size > settings.MAX_UPLOAD_SIZE:
                messages.error(request, 'Image file too large ( > 5MB )')
                return render(request, 'profile_completion.html')
                
            # Create image in Wagtail's image library
            image = Image.objects.create(
                title=f"{request.user.username}'s profile picture",
                file=photo
            )
            
            # Update author profile with the image
            author.photo = image
            author.save()
            
            # Update Wagtail user profile for SSO users
            from wagtail.users.models import UserProfile
            import os
            from django.core.files.base import ContentFile
            from django.core.files.storage import default_storage
            
            # Reset file pointer
            photo.seek(0)
            
            # Create a path for the avatar
            filename = f"user_{request.user.id}_avatar.jpg"
            avatar_path = os.path.join('user_avatars', filename)
            
            # Save the image to storage
            saved_path = default_storage.save(avatar_path, ContentFile(photo.read()))
            
            # Get or create the user profile
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            
            # Set the avatar path - not the file itself
            user_profile.avatar = saved_path
            user_profile.save()
            
            # Force refresh the user profile in the session
            request.user.wagtail_userprofile = user_profile
            
            messages.success(request, 'Profile updated successfully!')
        except Exception as e:
            messages.error(request, f'Error uploading image: {str(e)}')
            return render(request, 'profile_completion.html')

        # Clear the profile completion flag
        if 'needs_profile_completion' in request.session:
            del request.session['needs_profile_completion']

        return redirect('wagtail_serve', '')

    return render(request, 'profile_completion.html')