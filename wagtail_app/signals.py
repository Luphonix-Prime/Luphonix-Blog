from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from allauth.account.signals import user_signed_up
from wagtail.users.models import UserProfile
from wagtail.models import Page, GroupPagePermission, Collection, GroupCollectionPermission
from wagtail.images.models import Image
from wagtail.documents.models import Document
from wagtail_app.blog.models import Author
from django.contrib.contenttypes.models import ContentType

def ensure_author_group_and_permissions():
    # Create groups if they don't exist
    editor_group, _ = Group.objects.get_or_create(name='Editors')
    moderator_group, _ = Group.objects.get_or_create(name='Moderators')
    author_group, _ = Group.objects.get_or_create(name='Authors')

    # Get content types
    page_content_type = ContentType.objects.get_for_model(Page)
    collection_content_type = ContentType.objects.get_for_model(Collection)

    # Get or create root collection
    root_collection = Collection.objects.first()
    if not root_collection:
        root_collection = Collection.add_root(name='Root')

    # Base permissions
    base_permissions = {
        'editor': ['add_page', 'change_page', 'delete_page', 'publish_page'],
        'moderator': ['add_page', 'change_page', 'publish_page'],
        'author': ['add_page', 'change_page']
    }

    # Assign base permissions to groups
    for group_name, perms in base_permissions.items():
        group = locals()[f"{group_name}_group"]
        for perm in perms:
            try:
                permission = Permission.objects.get(
                    codename=perm,
                    content_type=page_content_type,
                )
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                pass

    # Add Wagtail specific group page permissions
    root_page = Page.objects.first()
    if root_page:
        # Get all required permissions
        add_permission = Permission.objects.get(codename='add_page', content_type=page_content_type)
        edit_permission = Permission.objects.get(codename='change_page', content_type=page_content_type)
        publish_permission = Permission.objects.get(codename='publish_page', content_type=page_content_type)

        # Moderator permissions
        GroupPagePermission.objects.get_or_create(
            group=moderator_group,
            page=root_page,
            permission=add_permission
        )
        GroupPagePermission.objects.get_or_create(
            group=moderator_group,
            page=root_page,
            permission=edit_permission
        )
        GroupPagePermission.objects.get_or_create(
            group=moderator_group,
            page=root_page,
            permission=publish_permission
        )

        # Author permissions
        GroupPagePermission.objects.get_or_create(
            group=author_group,
            page=root_page,
            permission=add_permission
        )
        GroupPagePermission.objects.get_or_create(
            group=author_group,
            page=root_page,
            permission=edit_permission
        )

    # Add collection permissions for images
    collection_permissions = {
        'editor': ['add', 'change', 'delete'],
        'moderator': ['add', 'change'],
        'author': ['add', 'change']
    }

    for group_name, perms in collection_permissions.items():
        group = locals()[f"{group_name}_group"]
        for perm_type in perms:
            try:
                GroupCollectionPermission.objects.get_or_create(
                    group=group,
                    collection=root_collection,
                    permission=Permission.objects.get(
                        codename=f"{perm_type}_image",
                        content_type=ContentType.objects.get(app_label='wagtailimages', model='image')
                    )
                )
            except Permission.DoesNotExist:
                pass

    return author_group

@receiver(user_signed_up)
def handle_user_signup(request, user, **kwargs):
    # Make user staff
    user.is_staff = True

    # Ensure last_name is set
    if not user.last_name:
        user.last_name = "notgiven"

    # Ensure groups and permissions exist, get Authors group
    author_group = ensure_author_group_and_permissions()

    # Add user to Authors group
    user.groups.add(author_group)

    # Add Wagtail admin access permission
    try:
        wagtail_admin_access = Permission.objects.get(
            codename='access_admin',
            content_type=ContentType.objects.get(app_label='wagtailadmin', model='admin')
        )
        user.user_permissions.add(wagtail_admin_access)
        print(f"[DEBUG] access_admin permission added to {user.username}")
    except Permission.DoesNotExist:
        print("[ERROR] wagtailadmin.access_admin permission does not exist! Run 'python manage.py migrate wagtailadmin'.")

    user.save()

    # Wagtail UserProfile
    UserProfile.objects.get_or_create(user=user)

    # Create or update Author model
    author, created = Author.objects.get_or_create(
        email=user.email,
        defaults={
            'name': user.username,
            'bio': request.POST.get('bio', '') if hasattr(request, 'POST') else '',
            'website': request.POST.get('website', '') if hasattr(request, 'POST') else '',
            'twitter': request.POST.get('twitter', '') if hasattr(request, 'POST') else '',
            'linkedin': request.POST.get('linkedin', '') if hasattr(request, 'POST') else ''
        }
    )
    if not created:
        author.name = user.username
        if hasattr(request, 'POST'):
            author.bio = request.POST.get('bio', '')
            author.website = request.POST.get('website', '')
            author.twitter = request.POST.get('twitter', '')
            author.linkedin = request.POST.get('linkedin', '')
        author.save()
    
    # Set a session flag to indicate profile completion is needed
    if hasattr(request, 'session'):
        request.session['needs_profile_completion'] = True


@receiver(post_delete, sender=get_user_model())
def delete_author_on_user_delete(sender, instance, **kwargs):
    """
    Signal handler to delete the associated Author when a User is deleted
    """
    try:
        # Try to find and delete the associated author
        Author.objects.filter(email=instance.email).delete()
    except Exception as e:
        print(f"Error deleting author for user {instance.username}: {str(e)}")
