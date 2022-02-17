from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from graphene import ObjectType, String

class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password',)

class TaskType(ObjectType, type):
    status = String()
    id = String()
