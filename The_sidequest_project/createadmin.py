from django.contrib.auth import get_user_model
from django.db import OperationalError

User = get_user_model()

try:
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="Lester James",
            password="L3st3r@315",
            email="ljamesceleste@gmail.com"
        )
        print("Superuser created.")
    else:
        print("Superuser already exists.")
except OperationalError:
    # Database not ready during migrations
    print("Could not create superuser (database not ready yet).")