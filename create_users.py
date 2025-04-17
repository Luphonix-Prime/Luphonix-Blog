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
from wagtail.models import Page, GroupPagePermission
from wagtail.core.permission_policies.pages import PagePermissionPolicy

User = get_user_model()

def create_user_groups():
    # Create groups if they don't exist
    editor_group, _ = Group.objects.get_or_create(name='Editors')
    moderator_group, _ = Group.objects.get_or_create(name='Moderators')
    author_group, _ = Group.objects.get_or_create(name='Authors')

    # Get content type for Page
    page_content_type = ContentType.objects.get_for_model(Page)

    # Define base permissions that exist in Django
    base_permissions = {
        'editor': ['add_page', 'change_page', 'delete_page'],
        'moderator': ['add_page', 'change_page'],
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
        # Editor permissions
        GroupPagePermission.objects.get_or_create(
            group=editor_group,
            page=root_page,
            permission_type='add'
        )
        GroupPagePermission.objects.get_or_create(
            group=editor_group,
            page=root_page,
            permission_type='edit'
        )
        GroupPagePermission.objects.get_or_create(
            group=editor_group,
            page=root_page,
            permission_type='publish'
        )

        # Moderator permissions
        GroupPagePermission.objects.get_or_create(
            group=moderator_group,
            page=root_page,
            permission_type='edit'
        )
        GroupPagePermission.objects.get_or_create(
            group=moderator_group,
            page=root_page,
            permission_type='publish'
        )

        # Author permissions
        GroupPagePermission.objects.get_or_create(
            group=author_group,
            page=root_page,
            permission_type='add'
        )
        GroupPagePermission.objects.get_or_create(
            group=author_group,
            page=root_page,
            permission_type='edit'
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
            'last_name': 'User1'
        },
        {
            'username': 'user2',
            'email': 'user2@luphonix.com',
            'password': 'user2password',
            'first_name': 'Regular',
            'last_name': 'User2'
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