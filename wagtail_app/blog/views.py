from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from taggit.models import Tag
from .models import BlogPage, Author
from django.urls import reverse
from wagtail.models import Page, GroupPagePermission, Collection, GroupCollectionPermission
from wagtail.images.models import Image
from wagtail.permission_policies.collections import CollectionPermissionPolicy
from wagtail.documents.models import Document
from wagtail.images.permissions import permission_policy as image_permission_policy
from wagtail.documents.permissions import permission_policy as document_permission_policy
from .models import Author

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Check if profile picture is provided
            if not request.FILES or 'profile_picture' not in request.FILES:
                form.add_error(None, "Profile picture is required")
                return render(request, 'registration/signup.html', {'form': form})
                
            user = form.save()
            
            # Create author profile
            author = Author.objects.create(
                name=user.username,
                bio=request.POST.get('bio', ''),
                email=request.POST.get('email', ''),
                website=request.POST.get('website', ''),
                twitter=request.POST.get('twitter', ''),
                linkedin=request.POST.get('linkedin', '')
            )
            
            # Handle profile picture upload
            profile_pic = request.FILES['profile_picture']
            # Create a Wagtail image
            image = Image.objects.create(
                title=f"{user.username}'s profile picture",
                file=profile_pic
            )
            # Assign the image to the author
            author.photo = image
            author.save()
            
            # Add user to Authors group
            authors_group, _ = Group.objects.get_or_create(name='Authors')
            user.groups.add(authors_group)
            
            # Set is_staff to True to allow admin access
            user.is_staff = True
            user.save()
            
            # Get content types
            page_content_type = ContentType.objects.get_for_model(Page)
            
            # Add base permissions for authors
            base_permissions = ['add_page', 'change_page']
            for perm in base_permissions:
                try:
                    permission = Permission.objects.get(
                        codename=perm,
                        content_type=page_content_type,
                    )
                    authors_group.permissions.add(permission)
                except Permission.DoesNotExist:
                    continue

            # Add Wagtail admin access permission
            wagtail_admin_access = Permission.objects.get(
                codename='access_admin',
                content_type=ContentType.objects.get(app_label='wagtailadmin', model='admin')
            )
            user.user_permissions.add(wagtail_admin_access)

            # Add group page permissions for the root page
            root_page = Page.objects.first()
            if root_page:
                add_permission = Permission.objects.get(codename='add_page', content_type=page_content_type)
                edit_permission = Permission.objects.get(codename='change_page', content_type=page_content_type)
                
                GroupPagePermission.objects.get_or_create(
                    group=authors_group,
                    page=root_page,
                    permission=add_permission
                )
                GroupPagePermission.objects.get_or_create(
                    group=authors_group,
                    page=root_page,
                    permission=edit_permission
                )

            # Add collection permissions for images
            root_collection = Collection.objects.first()
            if root_collection:
                for perm_type in ['add', 'change']:
                    try:
                        GroupCollectionPermission.objects.get_or_create(
                            group=authors_group,
                            collection=root_collection,
                            permission=Permission.objects.get(
                                codename=f"{perm_type}_image",
                                content_type=ContentType.objects.get(app_label='wagtailimages', model='image')
                            )
                        )
                    except Permission.DoesNotExist:
                        continue

            # Login the user
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('wagtail_serve', '')  # Redirect to homepage
        else:
            return render(request, 'registration/signup.html', {'form': form})
    return render(request, 'registration/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            
            # Check if there's a next parameter in the request
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('wagtail_serve', '')  # Redirect to homepage
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('wagtail_serve', '')  # Redirect to homepage

def tag_view(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = BlogPage.objects.live().filter(tags=tag)
    return render(request, 'blog/tag_page.html', {
        'tag': tag,
        'posts': posts,
    })


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Author

@login_required
def profile_completion(request):
    if request.method == 'POST':
        # Check if profile picture is provided
        if not request.FILES or 'profile_picture' not in request.FILES:
            messages.error(request, "Profile picture is required")
            return render(request, 'profile_completion.html')

        # Get form data
        bio = request.POST.get('bio', '')
        website = request.POST.get('website', '')
        twitter = request.POST.get('twitter', '')
        linkedin = request.POST.get('linkedin', '')
        photo = request.FILES.get('profile_picture')

        # Get or create author
        author, created = Author.objects.get_or_create(
            email=request.user.email,
            defaults={'name': request.user.username}
        )
        
        try:
            # Create image in Wagtail's image library
            image = Image.objects.create(
                title=f"{request.user.username}'s profile picture",
                file=photo
            )
            
            # Update author profile with the image
            author.photo = image
            author.bio = bio
            author.website = website
            author.twitter = twitter
            author.linkedin = linkedin
            author.save()
            
            # Update Wagtail user profile
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
            
            # Set the avatar path
            user_profile.avatar = saved_path
            user_profile.save()
            
            # Force refresh the user profile in the session
            request.user.wagtail_userprofile = user_profile
            
            messages.success(request, 'Profile completed successfully!')
        except Exception as e:
            messages.error(request, f"Error uploading profile picture: {str(e)}")
            return render(request, 'profile_completion.html')
        
        # Clear the profile completion flag
        request.session['needs_profile_completion'] = False
        
        return redirect('/')
        
    return render(request, 'profile_completion.html')