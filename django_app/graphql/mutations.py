from pydoc import describe
from graphene import Mutation, String, Field
from django_app.task import sample_task
from graphql_jwt.decorators import login_required
from .types import TaskType

class CreateSampleTaskMutation(Mutation):
    class Meta:
        description = 'Create a sample task to test out Celery delay task function'

    task = Field(TaskType)

    @classmethod
    @login_required
    def mutate(cls, root, info):
        task = sample_task.delay()
        return CreateSampleTaskMutation(task=task)
