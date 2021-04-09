from django.urls import path
from . import views

urlpatterns = [
    path('units/', views.getAllUnit, name="get_all_unit"),
    path('add_unit/', views.addUnit, name="add_unit"),

    path('unit/<int:unit_id>/', views.getUnitDetails,
         name="unit_details"),
    path('delete_unit/<int:unit_id>/', views.deleteUnit,
         name="delete_unit"),

    # Unit notes
    path('add_unit_note/<int:unit_id>/',
         views.addUnitNote, name="add_unit_note"),
    path('update_unit_note/<int:unit_note_id>/',
         views.updateUnitNote, name="update_unit_note"),
    path('delete_unit_note/<int:unit_note_id>/',
         views.deleteUnitNote, name="delete_unit_note"),

    # unit Documents
    # path('add_unit_document/<int:unit_id>/',
    #      views.addunitDocument, name="add_unit_document"),
    # path('delete_unit_document/<int:unit_doc_id>/',
    #      views.deleteunitDocument, name="delete_unit_document"),

]
