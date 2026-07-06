# accounts/management/commands/create_admin.py

from django.core.management.base import BaseCommand
from accounts.models import User, UserProfile

class Command(BaseCommand):
    help = 'Create admin user'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@syntaxacademy.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role=User.Role.ADMIN
            )
            UserProfile.objects.create(user=admin)
            self.stdout.write(self.style.SUCCESS('Admin user created successfully!'))
            self.stdout.write('Username: admin')
            self.stdout.write('Password: admin123')
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists!'))