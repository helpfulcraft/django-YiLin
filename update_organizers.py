import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welfare_config.settings')
django.setup()

from django.contrib.auth.models import User
from volunteerApp.models import VolunteerActivity

# Get the first admin user as default organizer
admin_user = User.objects.filter(is_superuser=True).first()

if admin_user:
    # Update all activities without an organizer
    activities = VolunteerActivity.objects.filter(organizer__isnull=True)
    for activity in activities:
        activity.organizer = admin_user
        activity.save()
    
    print(f"Updated {activities.count()} activities with default organizer.")
else:
    print("No admin user found to set as default organizer.")
