from django.contrib.auth.models import User
from celery.result import AsyncResult

class UserQueries:
    def all_users():
        return User.objects.all().order_by('email')

    def get_user(email):
        return User.objects.get(email=email)

class TaskQueries:
    def get_task_status(id):
        task_result = AsyncResult(id)
        return task_result
