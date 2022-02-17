from django.contrib.auth.models import User

class UserQueries:
    def all_users():
        return User.objects.all().order_by('email')

    def get_user(email):
        return User.objects.get(email=email)
