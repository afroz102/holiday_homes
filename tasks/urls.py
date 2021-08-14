from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.allTasks, name="get_all_task"),
    path('add_tasks/', views.addTask, name="add_task"),
    path('task_details/<int:task_id>/', views.taskDetails, name="task_details"),
    path('update_tasks_status/<int:task_id>/', views.updateTaskStatus,
         name="update_tasks_status"),
    path('add_task_manager/<int:task_id>/', views.addTaskManager,
         name="add_task_manager"),
    path('remove_task_manager/<int:task_manager_id>/',
         views.removeTaskManager, name="remove_task_manager"),
    path('update_task_manager_status/<int:task_manager_id>/',
         views.updateTaskManagerStatus, name="update_task_manager_status"),
]
