from django.urls import path

from TasksAPI.views import api_root, tasks_list, tasks_detail

urlpatterns = [
    path('', api_root, name='api-root'),
    path('tasks/', tasks_list, name='tasks-list'),
    path('tasks/<pk>', tasks_detail, name='task-detail'),
]
