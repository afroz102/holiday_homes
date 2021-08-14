from django.db import models
from django.contrib.auth.models import User
from users.models import UserCompany, UserProfile
from units.models import Unit
from bookings.models import Booking


class Task(models.Model):
    TASKSTATUS = (
        ('status_1', 'PENDING'),
        ('status_2', 'IN PROGRESS'),
        ('status_3', 'COMPLETED'),
        ('status_4', 'CANCELED'),
    )

    company = models.ForeignKey(
        UserCompany, on_delete=models.CASCADE, null=True)
    unit = models.ForeignKey(
        Unit, on_delete=models.SET_NULL, null=True, blank=True)
    booking = models.ForeignKey(
        Booking, on_delete=models.SET_NULL, null=True, blank=True)

    task_title = models.CharField(max_length=250, null=True, blank=True)
    task_details = models.TextField(null=True)
    task_date = models.DateField(null=True)
    task_time = models.TimeField(null=True)
    task_status = models.CharField(
        max_length=250, choices=TASKSTATUS, default='PENDING')
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.task_title


class TaskManager(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    assigned_to = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True)
    is_lead_manager = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
