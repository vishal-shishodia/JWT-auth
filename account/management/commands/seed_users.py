from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create sample users with various roles for UserProfile model"

    def handle(self, *args, **options):
        User = get_user_model()

        samples = [
            {"email": "admin@example.com", "first_name": "Admin", "last_name": "One", "mobile": "9999999999",
             "password": "Admin@123", "role": "Admin"},
            {"email": "legal@example.com", "first_name": "Legal", "last_name": "One", "mobile": "9999999998",
             "password": "Legal@123", "role": "Legal"},
            {"email": "pm@example.com", "first_name": "Project", "last_name": "Manager", "mobile": "9999999997",
             "password": "Pm@12345", "role": "PM"},
            {"email": "sales@example.com", "first_name": "Sales", "last_name": "One", "mobile": "9999999996",
             "password": "Sales@123", "role": "Sales"},
        ]

        for data in samples:
            if not User.objects.filter(email=data["email"]).exists():
                user = User(
                    email=data["email"],
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    mobile=data["mobile"],
                    role=data["role"]
                )
                user.set_password(data["password"])
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created {user.email} / {data['password']} ({user.role})"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"User {data['email']} already exists")
                )

        self.stdout.write(self.style.SUCCESS("Seeding done."))
