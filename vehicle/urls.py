from django.urls import path
from . import views

urlpatterns = [

    path("", views.vehicle_list, name="vehicle_list"),

    path("add/", views.add_vehicle, name="add_vehicle"),
    path("create/", views.add_vehicle, name="vehicle_create"),
    path("edit/<str:id>/", views.edit_vehicle, name="edit_vehicle"),
    path("delete/<str:id>/", views.delete_vehicle, name="delete_vehicle"),
]