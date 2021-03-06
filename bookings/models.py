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
        ('stage_1', 'Lead'),
        ('stage_2', 'Confirmed'),
        ('stage_3', 'Welcome Mail Sent'),
        ('stage_4', 'Document completed'),
        ('stage_5', 'Security Email'),
        ('stage_6', 'Checked In'),
        ('stage_7', 'Checkedout'),
    )

    company = models.ForeignKey(
        UserCompany, on_delete=models.CASCADE, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True)
    booking_source = models.CharField(
        max_length=250, choices=SOURCE, blank=True)
    # main_guest = models.OneToOneField(
    #     Guest, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=250, blank=True)
    country = models.CharField(max_length=250, blank=True)
    no_of_guest = models.CharField(max_length=250, blank=True)
    checkin_date = models.DateField(null=True, blank=True)
    checkout_date = models.DateField(null=True, blank=True)
    checkin_time = models.TimeField(null=True, blank=True)
    checkout_time = models.TimeField(null=True, blank=True)
    booking_status = models.CharField(
        max_length=250, default='Lead', choices=STATUS, blank=True)

    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    # is_canceled = models.BooleanField(default=False)
    # is_completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return 'booking-'+str(self.id)+'-'+self.unit.unit_name


class Guest(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    DOCTYPE = (
        ('Passport', 'Passport'),
        ('Emirates Id', 'Emirates Id'),
        ('Other', 'Other'),
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250, blank=True)
    email = models.CharField(max_length=250, blank=True)
    phone = models.CharField(max_length=250, blank=True)
    age = models.CharField(max_length=250, blank=True)
    gender = models.CharField(max_length=250, choices=GENDER, blank=True)
    document_type = models.CharField(
        max_length=250, choices=DOCTYPE, blank=True)
    file_one = models.FileField(upload_to='guest_doc/', null=True, blank=True)
    file_two = models.FileField(upload_to='guest_doc/', null=True, blank=True)

    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "Booking-" + str(self.booking.id) + '-Guest-' + self.name


class MainGuestBookingMapping(models.Model):
    company = models.ForeignKey(
        UserCompany, on_delete=models.CASCADE, null=True)
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, null=True)
    main_guest = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True)

    is_canceled = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "MainGuest-" + self.main_guest.name+'-' + self.booking.unit.unit_name+'-' + str(self.booking.id)


class BookingNote(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
    booking_note = models.TextField(blank=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "Booking-Note-" + str(self.id)


class ReOrderStringLogic(models.Model):
    company = models.OneToOneField(
        UserCompany, on_delete=models.CASCADE, null=True)
    stage_1 = models.TextField(blank=True)
    stage_2 = models.TextField(blank=True)
    stage_3 = models.TextField(blank=True)
    stage_4 = models.TextField(blank=True)
    stage_5 = models.TextField(blank=True)
    stage_6 = models.TextField(blank=True)
    stage_7 = models.TextField(blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.company.company_name + '-' + str(self.id) + '-order-logic'
