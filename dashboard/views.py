import csv
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse
from accounts.decorators import role_required
from accounts.models import CustomUser
from vehicle.models import Vehicle
from driver.models import Driver
from booking.models import Booking
from payment.models import Payment
from requests_app.models import PartnerRequest, DriverRequest


@role_required("ADMIN")
def admin_dashboard(request):
    customer_count      = CustomUser.objects.filter(role="CUSTOMER").count()
    partner_count       = CustomUser.objects.filter(role="PARTNER").count()
    driver_count        = Driver.objects.count()
    vehicle_count       = Vehicle.objects.count()
    booking_count       = Booking.objects.count()
    payment_count       = Payment.objects.count()
    available_vehicle   = Vehicle.objects.filter(is_available=True).count()

    # Pending requests badges
    partner_pending = PartnerRequest.objects.filter(status="PENDING").count()
    driver_pending  = DriverRequest.objects.filter(status="PENDING").count()

    # Booking status counts for donut chart
    pending_count   = Booking.objects.filter(status="PENDING").count()
    confirmed_count = Booking.objects.filter(status="CONFIRMED").count()
    completed_count = Booking.objects.filter(status="COMPLETED").count()
    cancelled_count = Booking.objects.filter(status="CANCELLED").count()

    # Recent bookings
    recent_bookings = list(Booking.objects.all())[-10:][::-1]

    # Total revenue
    all_payments = Payment.objects.all()
    total_revenue = sum(float(p.amount or 0) for p in all_payments)

    context = {
        "customer_count":    customer_count,
        "partner_count":     partner_count,
        "driver_count":      driver_count,
        "vehicle_count":     vehicle_count,
        "booking_count":     booking_count,
        "payment_count":     payment_count,
        "available_vehicle": available_vehicle,
        "partner_pending":   partner_pending,
        "driver_pending":    driver_pending,
        "pending_count":     pending_count,
        "confirmed_count":   confirmed_count,
        "completed_count":   completed_count,
        "cancelled_count":   cancelled_count,
        "recent_bookings":   recent_bookings,
        "total_revenue":     total_revenue,
    }
    return render(request, "admin/dashboard.html", context)


@role_required("ADMIN")
def admin_reports(request):
    export = request.GET.get("export")

    if export == "bookings":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="bookings.csv"'
        writer = csv.writer(response)
        writer.writerow(["ID", "Customer", "Vehicle", "Pickup", "Dropoff", "Fare", "Status", "Date"])
        for b in Booking.objects.all():
            writer.writerow([
                str(b.id), str(b.customer), str(b.vehicle),
                b.pickup_location, b.dropoff_location,
                b.total_fare, b.status, b.created_at,
            ])
        return response

    if export == "payments":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="payments.csv"'
        writer = csv.writer(response)
        writer.writerow(["ID", "Booking", "Amount", "Status", "Date"])
        for p in Payment.objects.all():
            writer.writerow([str(p.id), str(p.booking), p.amount, p.status, p.created_at])
        return response

    if export == "users":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="users.csv"'
        writer = csv.writer(response)
        writer.writerow(["Name", "Email", "Role", "Joined"])
        for u in CustomUser.objects.all():
            writer.writerow([u.display_name, u.email, u.role, u.date_joined])
        return response

    total_revenue   = sum(float(p.amount or 0) for p in Payment.objects.all())
    booking_count   = Booking.objects.count()
    customer_count  = CustomUser.objects.filter(role="CUSTOMER").count()
    driver_count    = Driver.objects.count()
    pending_count   = Booking.objects.filter(status="PENDING").count()
    confirmed_count = Booking.objects.filter(status="CONFIRMED").count()
    completed_count = Booking.objects.filter(status="COMPLETED").count()
    cancelled_count = Booking.objects.filter(status="CANCELLED").count()

    context = {
        "total_revenue":   total_revenue,
        "booking_count":   booking_count,
        "customer_count":  customer_count,
        "driver_count":    driver_count,
        "pending_count":   pending_count,
        "confirmed_count": confirmed_count,
        "completed_count": completed_count,
        "cancelled_count": cancelled_count,
        "partner_pending": PartnerRequest.objects.filter(status="PENDING").count(),
        "driver_pending":  DriverRequest.objects.filter(status="PENDING").count(),
    }
    return render(request, "admin/reports.html", context)