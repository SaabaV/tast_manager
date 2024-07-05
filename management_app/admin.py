from django.contrib import admin
from management_app.models import (
    Project,
    Task,
    Tag,
    ProjectFile
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_count_of_files', 'date_of_creation')  # центральное поле - сгенерированно функцией
    search_fields = ('name',)

    def display_count_of_files(self, obj):  # спец метод, который поможет для каждого проекта
        # получить список всех его файлов
        # этот метод применяется у нас в list_display чуть выше
        return obj.count_of_files

    display_count_of_files.short_description = 'Count of Files'  # название поля, которое будет видно в админ панели

    def replace_spaces_with_underscores(self, request, objects):  # наш личный admin action,
        # который позволит заменять пробелы на нижние подчёркивания у всех выделенных объектов
        for obj in objects:  # проходим по всем объектам
            obj.name = obj.name.replace(" ", "_")  # для каждого объекта обновляем поле name
            obj.save()  # сохраняем изменения
        return objects

    replace_spaces_with_underscores.short_description = 'Replace spaces with underscorses'

    actions = [replace_spaces_with_underscores]  # регистрируем список всех кастомных админ action

@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'file_path', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ('name', 'title')
    list_display = (
        'name',
        'project',
        'assignee',
        'status',
        'priority',
        'created_date',
        'due_date'
    )

    def change_status(self, request, objects):  # админ action, который позволит нам менять статус на closed
        for obj in objects:
            obj.status = 'Closed'
            obj.save()
        return objects

    # следующие методы ниже - админ action, которые позволят менять приоритетность у задач
    def change_priority_to_low(self, request, objects):
        for obj in objects:
            obj.priority = 'Low'
            obj.save()
        return objects

    def change_priority_to_medium(self, request, objects):
        for obj in objects:
            obj.priority = 'Medium'
            obj.save()
        return objects

    def change_priority_to_high(self, request, objects):
        for obj in objects:
            obj.priority = 'High'
            obj.save()
        return objects

    def change_priority_to_very_high(self, request, objects):
        for obj in objects:
            obj.priority = 'Very High'
            obj.save()
        return objects

    change_status.short_description = 'Mark as Closed'
    change_priority_to_low.short_description = 'Mark as Low priority'
    change_priority_to_medium.short_description = 'Mark as Medium priority'
    change_priority_to_high.short_description = 'Mark as High priority'
    change_priority_to_very_high.short_description = 'Mark as Very High priority'

    actions = [
        'change_status',
        'change_priority_to_low',
        'change_priority_to_medium',
        'change_priority_to_high',
        'change_priority_to_very_high',
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ...
