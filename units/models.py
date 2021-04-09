from django.db import models
from django.contrib.auth.models import User
from users.models import UserCompany
from landlords.models import Landlord


class Unit(models.Model):
    company = models.ForeignKey(
        UserCompany, on_delete=models.CASCADE, null=True)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, null=True)
    unit_name = models.CharField(max_length=250, blank=True)
    q1 = models.CharField(max_length=250, blank=True)
    q2 = models.CharField(max_length=250, blank=True)
    q3 = models.CharField(max_length=250, blank=True)
    q4 = models.CharField(max_length=250, blank=True)
    q5 = models.CharField(max_length=250, blank=True)
    q6 = models.CharField(max_length=250, blank=True)
    q7 = models.CharField(max_length=250, blank=True)
    q8 = models.CharField(max_length=250, blank=True)
    q9 = models.CharField(max_length=250, blank=True)

    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        if self.unit_name:
            return self.unit_name

        return str(self.id)


class UnitNote(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True)
    unit_note = models.TextField(blank=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "Unit-Note-" + str(self.id)
