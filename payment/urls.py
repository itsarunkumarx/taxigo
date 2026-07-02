from django.urls import path
from . import views

urlpatterns = [
    path("", views.payment_list, name="payment_list"),
    path(
        "add/<int:booking_id>/",
        views.make_payment,
        name="make_payment"
    ),
    
]