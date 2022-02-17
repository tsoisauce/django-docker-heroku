"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView

from .views import ping, index, create_task, get_task_status

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    # sample endpoint
    path('ping/', ping, name='ping'),
    # testing background task endpoints
    path('task', create_task, name='create_task'),
    path('task/<str:task_id>', get_task_status, name='get_task_status'),
    # database health checks django-health-check
    path('ht/', include('health_check.urls'), name='health_check'),
    # django-debug-toolbar
    path('__debug__/', include('debug_toolbar.urls')),
    # graphene-django
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
