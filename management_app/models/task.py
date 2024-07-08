#models/task.py
import calendar

from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions.datetime import datetime
from django.utils import timezone

from management_app.constants.choices_models import (
    STATUS_CHOICES,
    PRIORITY_CHOICES
)


def calculate_end_of_month() -> datetime:
    current_date = timezone.now()
    amount_of_days = calendar.monthrange(
        current_date.year,
        current_date.month)[1]
    date = datetime(
        year=current_date.year,
        month=current_date.month,
        day=amount_of_days,
    )
    return date.astimezone()


class Task(models.Model):
    name = models.CharField(max_length=120, unique=True, validators=[MinLengthValidator(10)])
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="new")
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default="Normal")
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks')
    tags = models.ManyToManyField('Tag', related_name='tasks')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(default=calculate_end_of_month)
    assignee = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Tasks'
        ordering = ['-due_date']
        unique_together = ('name', 'project')

    def __str__(self):
        return f"{self.name}, status: {self.status}"


class SubTask(models.Model):
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        unique_together = ['title']


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        unique_together = ['name']