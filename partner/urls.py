from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.partner_dashboard, name="partner_dashboard"),
]