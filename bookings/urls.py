from django.urls import path
from . import views

urlpatterns = [
    path('bookings/', views.getAllBooking, name="get_all_booking"),
    path('add_booking/', views.addBooking, name="add_booking"),

    path('booking/<int:booking_id>/', views.getBookingDetails,
         name="booking_details"),
    #     path('delete_booking/<int:booking_id>/', views.deleteBooking,
    #          name="delete_booking"),

]
