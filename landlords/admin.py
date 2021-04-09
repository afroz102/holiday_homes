from django.contrib import admin

from landlords.models import Landlord, LandlordDocument, LandlordNote

admin.site.register(Landlord)
admin.site.register(LandlordDocument)
admin.site.register(LandlordNote)
# admin.site.register(FranchiseProfileLog)
