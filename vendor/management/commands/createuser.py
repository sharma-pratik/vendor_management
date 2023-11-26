from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Create a new Django user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the new user')
        parser.add_argument('password', type=str, help='Password for the new user')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']

        # Check if the user with the given username already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR('User already exists with "{}" username.'.format(username)))
            return

        # Create the new user
        user = User.objects.create_user(username=username, password=password)

        token = Token.objects.create(user=user)

        self.stdout.write(self.style.SUCCESS("User created successfully and token is : {}".format(token)))
