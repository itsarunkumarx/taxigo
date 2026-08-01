from django.urls import path
from . import views

urlpatterns = [
    path("", views.driver_list, name="driver_list"),
    path("add/", views.add_driver, name="add_driver"),
    path("edit/<str:id>/", views.edit_driver, name="edit_driver"),
    path("delete/<str:id>/", views.delete_driver, name="delete_driver"),

    # Driver Ride Center & Navigation
    path("rides/", views.driver_rides, name="driver_rides"),
    path("accept/<str:booking_id>/", views.accept_ride, name="accept_ride"),
    path("reject/<str:booking_id>/", views.reject_ride, name="reject_ride"),
    path("start/<str:booking_id>/", views.start_ride, name="start_ride"),
    path("complete/<str:booking_id>/", views.complete_ride, name="complete_ride"),
    path("navigation/<str:booking_id>/", views.driver_navigation, name="driver_navigation"),

    # Sprint 6 Driver Earnings & Document Portal
    path("earnings/", views.driver_earnings, name="driver_earnings"),
    path("documents/", views.driver_documents, name="driver_documents"),
]