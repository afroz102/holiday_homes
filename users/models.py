from django.db import models
from django.contrib.auth.models import User


class UserCompany(models.Model):
    super_admin = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True)
    company_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200,  blank=True)
    email = models.CharField(max_length=200,  blank=True)
    address = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)

    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.company_name


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(
        UserCompany, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=200,  blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pic/', default="profile_pic/profile-dum.jpg",
        null=True, blank=True)

    is_deleted = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        if self.user.first_name:
            return self.user.first_name + '-' + self.user.last_name
        return str(self.id)

    @property
    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name


class UserToCompanyMapping(models.Model):
    ACCESSTYPE = (
        ('super-admin', 'super-admin'),
        ('admin', 'admin'),
        ('team-member', 'team-member'),
    )

    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(UserCompany,
                                on_delete=models.CASCADE, null=True)
    access_type = models.CharField(
        max_length=200, null=True, blank=True, choices=ACCESSTYPE)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        if self.user_profile.full_name:
            return self.company.company_name + '-' + self.user_profile.full_name

        return self.company.company_name + '-' + str(self.id)
