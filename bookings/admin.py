from django.contrib import admin
from bookings.models import Booking, BookingNote, Guest, MainGuestBookingMapping, ReOrderStringLogic

admin.site.register(Booking)
admin.site.register(BookingNote)
admin.site.register(Guest)
admin.site.register(MainGuestBookingMapping)
admin.site.register(ReOrderStringLogic)
