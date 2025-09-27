from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a default admin user for production'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Username for admin')
        parser.add_argument('--password', type=str, default='admin123', help='Password for admin')
        parser.add_argument('--email', type=str, default='admin@example.com', help='Email for admin')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists!')
            )
            return
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_staff=True,
            is_superuser=True
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created admin user: "{username}" with password: "{password}"'
            )
        )