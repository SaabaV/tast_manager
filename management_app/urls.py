from django.urls import path
from rest_framework.routers import DefaultRouter
from management_app.views import (
    get_all_projects,
    create_new_tag,
    get_all_tags,
    get_tag_by_id,
    TaskCreateView,
    TaskListView,
    TaskStatsView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    UserTaskListView
)

router = DefaultRouter()

urlpatterns = [
    path('projects/', get_all_projects),
    path('tags/', get_all_tags),
    path('tags/create/', create_new_tag),
    path('tags/<int:pk>/', get_tag_by_id),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    path('my-tasks/', UserTaskListView.as_view(), name='user-task-list'),
]

urlpatterns += router.urls



