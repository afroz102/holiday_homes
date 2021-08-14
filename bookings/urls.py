from django.urls import path
from . import views

urlpatterns = [
    path('bookings/', views.getAllBooking, name="get_all_booking"),
    path('add_booking/', views.addBooking, name="add_booking"),

    path('booking/<int:booking_id>/', views.getBookingDetails,
         name="booking_details"),
    path('cancel_booking/<int:booking_id>/', views.cancelBooking,
         name="cancel_booking"),
    path('booking_completed/<int:booking_id>/', views.bookingCompleted,
         name="booking_completed"),

    # guest Add/Update/Delete
    path('add_guest/<int:booking_id>/', views.addGuest,
         name="add_guest"),
    path('update_guest/<int:guest_id>/', views.updateGuest,
         name="update_guest"),
    path('delete_guest/<int:guest_id>/', views.deleteGuest,
         name="delete_guest"),

    # Note Add/Delete/Update
    path('add_note/<int:booking_id>/', views.addBookingNote,
         name="add_booking_note"),
    path('update_note/<int:booking_note_id>/', views.updateBookingNote,
         name="update_booking_note"),
    path('delete_note/<int:booking_note_id>/', views.deleteBookingNote,
         name="delete_booking_note"),

    path('update_booking_status/', views.updateBookingStatus,
         name='update_booking_status'),
    path('update_booking_status_in_profile/', views.updateBookingStatusInProfile,
         name='update_booking_status_in_profile'),
]
