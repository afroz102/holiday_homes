from django.db import models
from django.contrib.auth.models import User
from users.models import UserCompany
from units.models import Unit


class Booking(models.Model):
    SOURCE = (
        ('Source1', 'Source1'),
        ('Source2', 'Source2'),
        ('Source3', 'Source3'),
    )

    STATUS = (
        ('Status1', 'Status1'),
        ('Status2', 'Status2'),
        ('Status3', 'Status3'),
    )

    company = models.ForeignKey(
        UserCompany, on_delete=models.CASCADE, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True)
    booking_source = models.CharField(
        max_length=250, choices=SOURCE, blank=True)
    main_guest_name = models.CharField(max_length=250, blank=True)
    email = models.CharField(max_length=250, blank=True)
    phone = models.CharField(max_length=250, blank=True)
    address = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=250, blank=True)
    country = models.CharField(max_length=250, blank=True)
    checkin_date = models.DateField(null=True, blank=True)
    checkout_date = models.DateField(null=True, blank=True)
    checkin_time = models.TimeField(null=True, blank=True)
    checkout_time = models.TimeField(null=True, blank=True)
    booking_status = models.CharField(
        max_length=250, choices=STATUS, blank=True)

    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        if self.unit_name:
            return self.unit_name

        return str(self.id)


class Guest(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250, blank=True)
    email = models.CharField(max_length=250, blank=True)
    phone = models.CharField(max_length=250, blank=True)
    age = models.CharField(max_length=250, blank=True)
    gender = models.CharField(max_length=250, choices=GENDER, blank=True)
    document_type = models.CharField(max_length=250, blank=True)
    file_one = models.FileField(upload_to='guest_doc/', null=True, blank=True)
    file_two = models.FileField(upload_to='guest_doc/', null=True, blank=True)

    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "Booking-Note-" + str(self.id)


class BookingNote(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
    booking_note = models.TextField(blank=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "Booking-Note-" + str(self.id)