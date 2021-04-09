from django.urls import path
from . import views

urlpatterns = [
    path('landlords/', views.getAllLandlord, name="get_all_landlord"),
    path('add_landlord/', views.addLandlord, name="add_landlord"),

    path('landlord/<int:landlord_id>/', views.getLandlordProfile,
         name="landlord_profile"),
    path('delete_landlord/<int:landlord_id>/', views.deleteLandlord,
         name="delete_landlord"),

    # Landlord notes
    path('add_landlord_note/<int:landlord_id>/',
         views.addLandlordNote, name="add_landlord_note"),
    path('update_landlord_note/<int:landlord_note_id>/',
         views.updateLandlordNote, name="update_landlord_note"),
    path('delete_landlord_note/<int:landlord_note_id>/',
         views.deleteLandlordNote, name="delete_landlord_note"),

    # Landlord Documents
    path('add_landlord_document/<int:landlord_id>/',
         views.addLandlordDocument, name="add_landlord_document"),
    path('delete_landlord_document/<int:landlord_doc_id>/',
         views.deleteLandlordDocument, name="delete_landlord_document"),

]
