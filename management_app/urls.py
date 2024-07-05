from django.urls import path

from management_app.views import (
    get_all_projects,
    get_all_tags,
    get_tag_by_id,
    create_new_tag,
    TaskCreateView,
    TaskListView,
    TaskStatsView
)

urlpatterns = [
    path('projects/', get_all_projects),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('tags/', get_all_tags),
    path('tags/<int:pk>/', get_tag_by_id),
    path('tags/create/', create_new_tag)
]

