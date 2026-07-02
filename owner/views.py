from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def owner_dashboard(request):
    return render(request, "owner/dashboard.html")