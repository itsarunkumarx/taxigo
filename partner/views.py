from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def partner_dashboard(request):
    return render(request, "partner/dashboard.html")