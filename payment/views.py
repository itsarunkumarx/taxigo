from django.shortcuts import render, redirect, get_object_or_404
from booking.models import Booking
from .models import Payment
from .forms import PaymentForm


def payment_list(request):
    payments = Payment.objects.all()

    return render(request, "payment/payment_list.html", {
        "payments": payments
    })


def make_payment(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id)

    # Prevent duplicate payment
    if Payment.objects.filter(booking=booking).exists():
        return redirect("payment_list")

    if request.method == "POST":

        form = PaymentForm(request.POST)

        if form.is_valid():

            payment = form.save(commit=False)

            payment.booking = booking
            payment.amount = booking.total_fare
            payment.payment_status = "Paid"
            payment.transaction_id = f"TXN{booking.id}{booking.customer.id}"

            payment.save()

            return redirect("payment_list")

    else:
        form = PaymentForm()

    return render(request, "payment/payment_form.html", {
        "form": form,
        "booking": booking
    })