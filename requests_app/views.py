from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from accounts.decorators import role_required
from accounts.models import CustomUser
from .models import PartnerRequest, DriverRequest


# ── Public apply views ────────────────────────────────────────────────────────

def partner_apply(request):
    if request.method == "POST":
        PartnerRequest.objects.create(
            full_name     = request.POST.get("full_name", ""),
            email         = request.POST.get("email", ""),
            phone         = request.POST.get("phone", ""),
            business_name = request.POST.get("business_name", ""),
            num_vehicles  = request.POST.get("num_vehicles", 1),
            city          = request.POST.get("city", ""),
            message       = request.POST.get("message", ""),
        )
        return redirect("apply_success")
    return render(request, "requests_app/partner_apply.html")


def driver_apply(request):
    if request.method == "POST":
        DriverRequest.objects.create(
            full_name      = request.POST.get("full_name", ""),
            email          = request.POST.get("email", ""),
            phone          = request.POST.get("phone", ""),
            license_number = request.POST.get("license_number", ""),
            vehicle_pref   = request.POST.get("vehicle_pref", ""),
            city           = request.POST.get("city", ""),
            experience_yrs = request.POST.get("experience_yrs", 0),
        )
        return redirect("apply_success")
    return render(request, "requests_app/driver_apply.html")


def apply_success(request):
    return render(request, "requests_app/apply_success.html")


# ── Admin management views ────────────────────────────────────────────────────

@role_required("ADMIN")
def admin_partner_requests(request):
    status_filter = request.GET.get("status", "ALL").upper()
    qs = PartnerRequest.objects.all()
    if status_filter != "ALL":
        qs = qs.filter(status=status_filter)

    if request.method == "POST":
        req_id = request.POST.get("req_id")
        action = request.POST.get("action", "").upper()
        pr = get_object_or_404(PartnerRequest, id=req_id)

        if action == "APPROVE":
            username = pr.email
            user = CustomUser.objects.filter(username=username).first()
            if not user:
                user = CustomUser.objects.create(
                    username   = username,
                    email      = username,
                    first_name = pr.full_name.split()[0],
                    last_name  = " ".join(pr.full_name.split()[1:]),
                    phone      = pr.phone,
                    role       = "PARTNER",
                    is_active  = True,
                )
            user.set_password("Taxigo@123")
            user.role = "PARTNER"
            user.is_active = True
            user.save()

            pr.status = "APPROVED"
            pr.save()
            messages.success(request, f"🎉 Partner account approved for {pr.full_name}! Login Email: {pr.email} | Password: Taxigo@123")

        elif action == "REJECT":
            pr.status = "REJECTED"
            pr.reject_reason = request.POST.get("reason", "")
            pr.save()
            messages.warning(request, f"Application from {pr.full_name} rejected.")

        return redirect("/admin-panel/partner-requests/")

    pending_count = PartnerRequest.objects.filter(status="PENDING").count()
    return render(request, "requests_app/admin_partner_requests.html", {
        "requests": qs,
        "status_filter": status_filter,
        "pending_count": pending_count,
        "total_count": PartnerRequest.objects.count(),
        "approved_count": PartnerRequest.objects.filter(status="APPROVED").count(),
        "rejected_count": PartnerRequest.objects.filter(status="REJECTED").count(),
    })


@role_required("ADMIN")
def admin_driver_requests(request):
    status_filter = request.GET.get("status", "ALL").upper()
    qs = DriverRequest.objects.all()
    if status_filter != "ALL":
        qs = qs.filter(status=status_filter)

    if request.method == "POST":
        req_id = request.POST.get("req_id")
        action = request.POST.get("action", "").upper()
        dr = get_object_or_404(DriverRequest, id=req_id)

        if action == "APPROVE":
            username = dr.email
            user = CustomUser.objects.filter(username=username).first()
            if not user:
                user = CustomUser.objects.create(
                    username   = username,
                    email      = username,
                    first_name = dr.full_name.split()[0],
                    last_name  = " ".join(dr.full_name.split()[1:]) if len(dr.full_name.split()) > 1 else "",
                    phone      = dr.phone,
                    role       = "DRIVER",
                    is_active  = True,
                )
            user.set_password("Taxigo@123")
            user.role = "DRIVER"
            user.is_active = True
            user.save()

            # Ensure Driver model profile exists and is linked
            from driver.models import Driver
            partner_user = CustomUser.objects.filter(role="PARTNER").first() or request.user
            driver_profile = Driver.objects.filter(user=user).first()
            if not driver_profile:
                Driver.objects.create(
                    partner=partner_user,
                    user=user,
                    full_name=dr.full_name,
                    gender="Male",
                    dob="1995-01-01",
                    mobile=dr.phone,
                    email=dr.email,
                    address=dr.city or "India",
                    aadhaar_number="123456789012",
                    license_number=dr.license_number or "DL1420110012345",
                    license_expiry="2030-12-31",
                    experience=getattr(dr, "experience_yrs", 1) or 1,
                    verification_status="APPROVED",
                    status="Active",
                )

            dr.status = "APPROVED"
            dr.save()
            messages.success(request, f"🎉 Driver account approved for {dr.full_name}! Login Email: {dr.email} | Default Password: Taxigo@123")

        elif action == "REJECT":
            dr.status = "REJECTED"
            dr.reject_reason = request.POST.get("reason", "")
            dr.save()
            messages.warning(request, f"Application from {dr.full_name} rejected.")

        return redirect("/admin-panel/driver-requests/")

    pending_count = DriverRequest.objects.filter(status="PENDING").count()
    return render(request, "requests_app/admin_driver_requests.html", {
        "requests": qs,
        "status_filter": status_filter,
        "pending_count": pending_count,
        "total_count": DriverRequest.objects.count(),
        "approved_count": DriverRequest.objects.filter(status="APPROVED").count(),
        "rejected_count": DriverRequest.objects.filter(status="REJECTED").count(),
    })


@role_required("ADMIN")
def admin_dashboard_redirect(request):
    return redirect("admin_dashboard")


@role_required("ADMIN")
def admin_users(request):
    role_filter = request.GET.get("role", "ALL")
    search = request.GET.get("search", "")
    qs = CustomUser.objects.all()
    if role_filter != "ALL":
        qs = qs.filter(role=role_filter)
    if search:
        qs = [u for u in qs if search.lower() in u.display_name.lower() or search.lower() in (u.email or "").lower()]
    return render(request, "requests_app/admin_users.html", {
        "users": qs,
        "role_filter": role_filter,
        "search": search,
    })


@role_required("ADMIN")
def admin_user_edit(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        new_role = request.POST.get("new_role") or request.POST.get("role")
        if new_role:
            user.role = new_role
            user.save()
            messages.success(request, f"Updated role for {user.display_name} to {new_role}")
    return redirect("admin_users")


@role_required("ADMIN")
def admin_user_toggle_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        user.is_active = not user.is_active
        user.save()
        status_str = "activated" if user.is_active else "deactivated"
        messages.success(request, f"User {user.display_name} has been {status_str}.")
    return redirect("admin_users")


from booking.models import PricingRule, Coupon
from booking.pricing import seed_default_pricing_rules

@role_required("ADMIN")
def admin_pricing(request):
    seed_default_pricing_rules()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_rule":
            rule_id = request.POST.get("rule_id")
            rule = get_object_or_404(PricingRule, id=rule_id)
            rule.base_fare = request.POST.get("base_fare", rule.base_fare)
            rule.rate_per_km = request.POST.get("rate_per_km", rule.rate_per_km)
            rule.rate_per_min = request.POST.get("rate_per_min", rule.rate_per_min)
            rule.surge_multiplier = request.POST.get("surge_multiplier", rule.surge_multiplier)
            rule.night_charge_percent = request.POST.get("night_charge_percent", rule.night_charge_percent)
            rule.airport_flat_charge = request.POST.get("airport_flat_charge", rule.airport_flat_charge)
            rule.is_active = request.POST.get("is_active") == "on"
            rule.save()
            messages.success(request, f"Updated pricing rule for {rule.display_name}")

        elif action == "add_coupon":
            code = request.POST.get("code", "").strip().upper()
            pct = request.POST.get("discount_percent", 10)
            max_amt = request.POST.get("max_discount_amount", 100)
            min_fare = request.POST.get("min_trip_fare", 0)
            if code:
                Coupon.objects.create(
                    code=code,
                    discount_percent=pct,
                    max_discount_amount=max_amt,
                    min_trip_fare=min_fare,
                    is_active=True
                )
                messages.success(request, f"Added promo coupon {code}")

        elif action == "toggle_coupon":
            coupon_id = request.POST.get("coupon_id")
            cp = get_object_or_404(Coupon, id=coupon_id)
            cp.is_active = not cp.is_active
            cp.save()
            messages.success(request, f"Coupon {cp.code} status updated.")

        return redirect("admin_pricing")

    rules = PricingRule.objects.all().order_by("id")
    coupons = Coupon.objects.all().order_by("-created_at")

    return render(request, "requests_app/admin_pricing.html", {
        "rules": rules,
        "coupons": coupons,
    })


@role_required("ADMIN")
def admin_documents(request):
    """
    Admin Driver Document Verification Panel.
    """
    from driver.models import Driver

    if request.method == "POST":
        driver_id = request.POST.get("driver_id")
        action = request.POST.get("action")  # "APPROVE" or "REJECT"
        reason = request.POST.get("reason", "").strip()

        driver = get_object_or_404(Driver, id=driver_id)
        if action == "APPROVE":
            driver.verification_status = "APPROVED"
            driver.rejection_reason = ""
            driver.save()
            messages.success(request, f"Approved documents for {driver.full_name}.")
        elif action == "REJECT":
            driver.verification_status = "REJECTED"
            driver.rejection_reason = reason or "Documents incomplete or invalid copy."
            driver.save()
            messages.error(request, f"Rejected documents for {driver.full_name}.")

        return redirect("admin_documents")

    status_filter = request.GET.get("status", "PENDING")
    drivers_qs = Driver.objects.all()
    if status_filter != "ALL":
        drivers_qs = drivers_qs.filter(verification_status=status_filter)

    return render(request, "requests_app/admin_documents.html", {
        "drivers": drivers_qs,
        "status_filter": status_filter,
        "pending_count": Driver.objects.filter(verification_status="PENDING").count(),
    })


@role_required("ADMIN")
def admin_sos_alerts(request):
    """
    Admin Emergency SOS Operations Center.
    """
    from booking.models import EmergencyAlert

    if request.method == "POST":
        alert_id = request.POST.get("alert_id")
        alert = get_object_or_404(EmergencyAlert, id=alert_id)
        alert.status = "RESOLVED"
        alert.save()
        messages.success(request, f"Emergency SOS Alert #{alert.id} marked as RESOLVED.")
        return redirect("admin_sos_alerts")

    alerts = EmergencyAlert.objects.all().order_by("-created_at")
    active_count = EmergencyAlert.objects.filter(status="ACTIVE").count()

    return render(request, "requests_app/admin_sos.html", {
        "alerts": alerts,
        "active_count": active_count,
    })



