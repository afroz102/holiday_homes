from django.contrib import admin
from bookings.models import Booking, BookingNote, Guest

admin.site.register(Booking)
admin.site.register(BookingNote)
admin.site.register(Guest)
