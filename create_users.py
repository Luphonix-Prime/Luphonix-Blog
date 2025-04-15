#!/usr/bin/env python
import os
import django
import sys
from django.db.utils import IntegrityError
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wagtail_app.settings')

try:
    django.setup()
except Exception as e:
    print(f"Error setting up Django environment: {e}")
    sys.exit(1)

from django.contrib.auth import get_user_model
User = get_user_model()

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
    staff_users = [
        {
            'username': 'editor',
            'email': 'editor@luphonix.com',
            'password': 'editorpassword',
            'first_name': 'Editor',
            'last_name': 'User',
            'is_staff': True
        },
        {
            'username': 'moderator',
            'email': 'moderator@luphonix.com',
            'password': 'moderatorpassword',
            'first_name': 'Moderator',
            'last_name': 'User',
            'is_staff': True
        }
    ]

    for user_data in staff_users:
        try:
            username = user_data.pop('username')
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    last_login=timezone.now(),
                    **user_data
                )
                print(f"Staff user '{username}' created successfully!")
            else:
                print(f"Staff user '{username}' already exists!")
        except Exception as e:
            print(f"Error creating staff user '{username}': {e}")

def create_regular_users():
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