from django.urls import path
from . import views

urlpatterns = [
    path("", views.driver_list, name="driver_list"),          # Driver List
    path("dashboard/", views.driver_dashboard, name="driver_dashboard"),
    path("add/", views.add_driver, name="add_driver"),
    path("edit/<int:id>/", views.edit_driver, name="edit_driver"),
    path("delete/<int:id>/", views.delete_driver, name="delete_driver"),
    path("rides/", views.driver_rides, name="driver_rides"),
    path("accept/<int:booking_id>/", views.accept_ride, name="accept_ride"),
    path("start/<int:booking_id>/", views.start_ride, name="start_ride"),
    path("complete/<int:booking_id>/", views.complete_ride, name="complete_ride"),
]