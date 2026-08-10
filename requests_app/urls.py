from django.urls import path
from . import views

urlpatterns = [
    # Public apply forms
    path("become-a-partner/", views.partner_apply, name="partner_apply"),
    path("become-a-driver/",  views.driver_apply,  name="driver_apply"),
    path("partner-apply/",    views.partner_apply),
    path("driver-apply/",     views.driver_apply),
    path("apply/success/",    views.apply_success,  name="apply_success"),

    # Admin management
    path("admin-panel/",                  views.admin_dashboard_redirect, name="admin_panel_index"),
    path("admin-panel/partner-requests/", views.admin_partner_requests,   name="admin_partner_requests"),
    path("admin-panel/driver-requests/",  views.admin_driver_requests,    name="admin_driver_requests"),
    path("admin-panel/users/",            views.admin_users,              name="admin_users"),
    path("admin-panel/users/<str:user_id>/edit/", views.admin_user_edit,  name="admin_user_edit"),
    path("admin-panel/users/<str:user_id>/toggle-status/", views.admin_user_toggle_status, name="admin_user_toggle_status"),
    path("admin-panel/pricing/",          views.admin_pricing,           name="admin_pricing"),
    path("admin-panel/documents/",        views.admin_documents,         name="admin_documents"),
    path("admin-panel/sos/",              views.admin_sos_alerts,        name="admin_sos_alerts"),
]
