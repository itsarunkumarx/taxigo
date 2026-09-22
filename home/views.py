from django.shortcuts import render
from django.contrib import messages

def home(request):
    return render(request, "home/index.html")

def about(request):
    return render(request, "about.html")

def services(request):
    return render(request, "services.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        messages.success(request, f"Thank you {name or 'for contacting us'}! Your message has been received. Our team will get back to you shortly.")
    return render(request, "contact.html")