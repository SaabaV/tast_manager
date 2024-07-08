from django.urls import path, include
from rest_framework.routers import DefaultRouter
from management_app.views import (
    get_all_projects,
    get_all_tags,
    get_tag_by_id,
    create_new_tag,
    TaskCreateView,
    TaskListView,
    TaskStatsView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    CategoryViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('projects/', get_all_projects),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('tags/', get_all_tags),
    path('tags/<int:pk>/', get_tag_by_id),
    path('tags/create/', create_new_tag),
    path('', include(router.urls)),
]

