import os
import django
from django.contrib.auth import get_user_model
from django.core.management import call_command

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wagtail_app.settings")
django.setup()

User = get_user_model()

def create_superuser():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User'
        )
        print("Superuser 'admin' created successfully!")
    else:
        print("Superuser 'admin' already exists!")

def create_staff_users():
    staff_users = [
        {
            'username': 'editor',
            'email': 'editor@example.com',
            'password': 'editorpassword',
            'first_name': 'Editor',
            'last_name': 'User',
            'is_staff': True
        },
        {
            'username': 'moderator',
            'email': 'moderator@example.com',
            'password': 'moderatorpassword',
            'first_name': 'Moderator',
            'last_name': 'User',
            'is_staff': True
        }
    ]

    for user_data in staff_users:
        username = user_data.pop('username')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, **user_data)
            print(f"Staff user '{username}' created successfully!")
        else:
            print(f"Staff user '{username}' already exists!")

def create_regular_users():
    regular_users = [
        {
            'username': 'user1',
            'email': 'user1@example.com',
            'password': 'user1password',
            'first_name': 'Regular',
            'last_name': 'User1'
        },
        {
            'username': 'user2',
            'email': 'user2@example.com',
            'password': 'user2password',
            'first_name': 'Regular',
            'last_name': 'User2'
        }
    ]

    for user_data in regular_users:
        username = user_data.pop('username')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, **user_data)
            print(f"Regular user '{username}' created successfully!")
        else:
            print(f"Regular user '{username}' already exists!")

if __name__ == '__main__':
    print("Creating users...")
    create_superuser()
    create_staff_users()
    create_regular_users()
    print("User creation completed!")