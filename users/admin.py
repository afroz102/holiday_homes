from django.contrib import admin

from users.models import UserCompany, UserProfile, UserToCompanyMapping

admin.site.register(UserCompany)
admin.site.register(UserProfile)
admin.site.register(UserToCompanyMapping)
