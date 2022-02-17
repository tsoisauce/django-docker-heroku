from graphene import ObjectType, Schema, Field, List, String
from graphql_jwt import ObtainJSONWebToken, Verify, Refresh, DeleteJSONWebTokenCookie, DeleteRefreshTokenCookie
from graphql_jwt.decorators import login_required
from .types import UserType, TaskType
from .queries import UserQueries, TaskQueries
from .mutations import CreateSampleTaskMutation

class Query(ObjectType):
    hello = String(default_value="Hello World!")
    whoami = Field(UserType)
    users = List(UserType)
    get_task_status = Field(TaskType, id=String(required=True))

    @login_required
    def resolve_whoami(self, info, **kwargs):
        return info.context.user

    @login_required
    def resolve_users(self, info, **kwargs):
        return UserQueries.all_users()
    
    @login_required
    def resolve_get_user(self, info, email):
        return UserQueries.get_user(email)

    @login_required
    def resolve_get_task_status(self, info, id):
        return TaskQueries.get_task_status(id)

class Mutation(ObjectType):
    # auth mutations
    token_auth = ObtainJSONWebToken.Field()
    verify_token = Verify.Field()
    refresh_token = Refresh.Field()
    delete_token_cookie = DeleteJSONWebTokenCookie.Field()
    delete_refresh_token_cookie = DeleteRefreshTokenCookie.Field()
    # sample task mutations
    create_sample_task = CreateSampleTaskMutation.Field()

schema = Schema(query=Query, mutation=Mutation)
