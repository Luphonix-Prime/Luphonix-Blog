#!/usr/bin/env python
import os
import django
import sys
from django.db.utils import IntegrityError
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wagtail_app.settings')
django.setup()  # Setup Django first

# Now import the models after Django is configured
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from wagtail.models import Page, GroupPagePermission, GroupCollectionPermission, Collection
from wagtail.permission_policies.pages import PagePermissionPolicy

User = get_user_model()

def create_user_groups():
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

    # Update base permissions
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
                print(f"Permission {perm} not found, skipping...")

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
            GroupCollectionPermission.objects.get_or_create(
                group=group,
                collection=root_collection,
                permission=Permission.objects.get(
                    codename=f"{perm_type}_image",
                    content_type=ContentType.objects.get(app_label='wagtailimages', model='image')
                )
            )

    return editor_group, moderator_group, author_group

def create_superuser():
    try:
        admin_user = User.objects.create_superuser(
            username='luphonix_prime_admin',
            email='Luphonix.prime@gmail.com',
            password='keval_dhyey#2025',
            first_name='Admin',
            last_name='User',
            last_login=timezone.now(),
        )
        print("Superuser 'luphonix_prime_admin' created successfully!")
    except IntegrityError:
        print("Superuser 'luphonix_prime_admin' already exists!")
    except Exception as e:
        print(f"Error creating superuser: {e}")

def create_staff_users():
    editor_group, moderator_group, _ = create_user_groups()
    
    staff_users = [
        {
            'username': 'editor',
            'email': 'editor@luphonix.com',
            'password': 'editorpassword',
            'first_name': 'Editor',
            'last_name': 'User',
            'is_staff': True,
            'group': editor_group
        },
        {
            'username': 'moderator',
            'email': 'moderator@luphonix.com',
            'password': 'moderatorpassword',
            'first_name': 'Moderator',
            'last_name': 'User',
            'is_staff': True,
            'group': moderator_group
        }
    ]

    for user_data in staff_users:
        try:
            group = user_data.pop('group')
            username = user_data.pop('username')
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    last_login=timezone.now(),
                    **user_data
                )
                user.groups.add(group)
                print(f"Staff user '{username}' created successfully!")
            else:
                print(f"Staff user '{username}' already exists!")
        except Exception as e:
            print(f"Error creating staff user '{username}': {e}")

def create_regular_users():
    _, _, author_group = create_user_groups()
    
    regular_users = [
        {
            'username': 'user1',
            'email': 'user1@luphonix.com',
            'password': 'user1password',
            'first_name': 'Regular',
            'last_name': 'User1',
            'is_staff': True  # Add this to allow admin access
        },
        {
            'username': 'user2',
            'email': 'user2@luphonix.com',
            'password': 'user2password',
            'first_name': 'Regular',
            'last_name': 'User2',
            'is_staff': True  # Add this to allow admin access
        }
    ]

    for user_data in regular_users:
        try:
            username = user_data.pop('username')
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    last_login=timezone.now(),
                    **user_data
                )
                user.groups.add(author_group)
                
                # Add Wagtail admin access permission
                wagtail_admin_access = Permission.objects.get(
                    codename='access_admin',
                    content_type=ContentType.objects.get(app_label='wagtailadmin', model='admin')
                )
                user.user_permissions.add(wagtail_admin_access)
                
                print(f"Regular user '{username}' created successfully!")
            else:
                print(f"Regular user '{username}' already exists!")
        except Exception as e:
            print(f"Error creating regular user '{username}': {e}")

if __name__ == '__main__':
    print("Starting user creation process...")
    try:
        create_superuser()
        create_staff_users()
        create_regular_users()
        print("User creation process completed successfully!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)