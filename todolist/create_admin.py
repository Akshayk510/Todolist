import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todolist.settings')
django.setup()

from django.contrib.auth.models import User

# Check if admin user already exists
if not User.objects.filter(username='admin').exists():
    # Create a superuser
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print("Admin user created successfully!")
    print("Username: admin")
    print("Password: admin123")
else:
    print("Admin user already exists.")