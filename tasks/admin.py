from django.contrib import admin
from tasks.models import Task, TaskManager

admin.site.register(Task)
admin.site.register(TaskManager)
