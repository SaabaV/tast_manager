import os
import django
from datetime import timedelta
from django.utils import timezone


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_management.settings")
django.setup()

from management_app.models.task import SubTask, Task
from management_app.models import Project


project = Project.objects.first()
if project is None:
    print("No project found. Please create a project first.")
else:
    task = Task.objects.create(
        name="Prepare presentation",
        description="Prepare materials and slides for the presentation",
        status="new",
        due_date=timezone.now() + timedelta(days=3),
        project=project
    )

    subtask1 = SubTask.objects.create(
        task=task,
        title="Gather information",
        description="Find necessary information for the presentation",
        status="new",
        deadline=timezone.now() + timedelta(days=2)
    )

    subtask2 = SubTask.objects.create(
        task=task,
        title="Create slides",
        description="Create presentation slides",
        status="new",
        deadline=timezone.now() + timedelta(days=1)
    )

    new_tasks = Task.objects.filter(status="new")
    print("Tasks with status 'New':")
    for task in new_tasks:
        print(task)

    overdue_done_subtasks = SubTask.objects.filter(status="Done", deadline__lt=timezone.now())
    print("\nOverdue SubTasks with status 'Done':")
    for subtask in overdue_done_subtasks:
        print(subtask)

    task = Task.objects.get(name="Prepare presentation")
    task.status = "in progress"
    task.save()

    subtask1 = SubTask.objects.get(title="Gather information", task__name="Prepare presentation")
    subtask1.deadline = timezone.now() - timedelta(days=2)
    subtask1.save()

    subtask2 = SubTask.objects.get(title="Create slides", task__name="Prepare presentation")
    subtask2.description = "Create and format presentation slides"
    subtask2.save()

    task = Task.objects.get(name="Prepare presentation")
    task.delete()

    print("\nTasks and SubTasks updated and deleted.")

