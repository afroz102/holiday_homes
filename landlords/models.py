from django.db import models
from django.contrib.auth.models import User
from users.models import UserCompany
# from users.models import


class Landlord(models.Model):
    # managed userAgency updated
    managed_by = models.ForeignKey(
        UserCompany, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250,  blank=True)
    phone = models.CharField(max_length=250, blank=True)
    local_address = models.CharField(max_length=250, blank=True)
    local_city = models.CharField(max_length=250, blank=True)
    local_country = models.CharField(max_length=250, blank=True)
    native_address = models.CharField(max_length=250, blank=True)
    native_city = models.CharField(max_length=250, blank=True)
    native_country = models.CharField(max_length=250, blank=True)

    bank_name = models.CharField(max_length=250, blank=True)
    branch_name = models.CharField(max_length=250, blank=True)
    bank_account_details = models.CharField(max_length=250, blank=True)
    ifsc_code = models.CharField(max_length=250, blank=True)

    status = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class LandlordDocument(models.Model):
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, null=True)
    doc_name = models.CharField(max_length=250, blank=True)
    doc_file = models.FileField(
        upload_to='landlord_doc/', null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.doc_name


class LandlordNote(models.Model):
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, null=True)
    landlord_note = models.TextField(null=True, blank=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        # return str(self.id)
        return self.landlord.name + "-Note-" + str(self.id)


# class LandlordProfileLog(models.Model):
#     landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, null=True)
#     updated_by = models.ForeignKey(
#         User, on_delete=models.CASCADE, null=True)
#     landlord_profile_log = models.TextField(null=True, blank=True)

#     date_created = models.DateTimeField(auto_now_add=True, null=True)
#     date_updated = models.DateTimeField(auto_now=True, null=True)

#     def __str__(self):
#         return self.landlord.name + "-report-" + str(self.id)
