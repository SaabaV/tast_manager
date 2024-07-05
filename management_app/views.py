from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q
import datetime

from management_app.models import Project, Tag
from management_app.serializers.projects import AllProjectsSerializer
from management_app.serializers.tags import AllTagsSerializer
from .models import Task
from serializers.tasks import AllTasksSerializer


@api_view(["GET"])
def get_all_projects(request: Request) -> Response:
    projects = Project.objects.all()
    if not projects.exists():
        return Response(data=[], status=status.HTTP_204_NO_CONTENT)
    serialize = AllProjectsSerializer(projects, many=True)

    return Response(data=serialize.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_new_tag(request: Request) -> Response:
    tag_data = request.data
    serializer = AllTagsSerializer(data=tag_data)

    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_all_tags(request: Request) -> Response:
    tags = Tag.objects.all()
    if not tags.exists():
        return Response(data=[], status=status.HTTP_204_NO_CONTENT)
    serialize = AllTagsSerializer(tags, many=True)

    return Response(data=serialize.data, status=status.HTTP_200_OK)


@api_view(["Get"])
def get_tag_by_id(request: Request, pk: int) -> Response:
    try:
        tag_by_id = Tag.objects.get(pk=pk)
    except Tag.DoesNotExist:
        return Response(data={}, status=status.HTTP_204_NO_CONTENT)

    serialize = AllTagsSerializer(tag_by_id)
    return Response(data=serialize.data, status=status.HTTP_200_OK)


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = AllTasksSerializer


class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = AllTasksSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    ordering_fields = ['deadline']
    ordering = ['deadline']


class TaskStatsView(APIView):
    def get(self, request, *args, **kwargs):
        total_tasks = Task.objects.count()
        status_counts = Task.objects.values('status').annotate(count=Count('status'))
        overdue_tasks = Task.objects.filter(deadline__lt=datetime.now(), status__ne='Done').count()

        stats = {
            'total_tasks': total_tasks,
            'status_counts': status_counts,
            'overdue_tasks': overdue_tasks,
        }
        return Response(stats)