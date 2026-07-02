import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Taxigo.settings')
django.setup()

from accounts.models import CustomUser

try:
    if not CustomUser.objects.filter(username='adminbala').exists():
        CustomUser.objects.create_superuser('adminbala', 'admin@taxigo.com', 'bala@2003')
        print("Superuser adminbala created successfully.")
    else:
        print("Superuser adminbala already exists.")
except Exception as e:
    print(f"Error creating superuser: {e}")
