import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Taxigo.settings')
django.setup()

from accounts.models import CustomUser

try:
    user = CustomUser.objects.filter(username='adminbala').first()
    if not user:
        CustomUser.objects.create_superuser(
            username='adminbala',
            email='admin@taxigo.com',
            password='bala@2003',
            role='ADMIN'
        )
        print("Superuser adminbala created successfully with role ADMIN.")
    else:
        user.role = 'ADMIN'
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print("Superuser adminbala verified and updated to role ADMIN.")
except Exception as e:
    print(f"Error creating/updating superuser: {e}")
