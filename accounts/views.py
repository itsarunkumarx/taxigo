from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    return render(request, "home.html")


def register(request):

    if request.method == "POST":

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        role = request.POST["role"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        # Check Password
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Check Username
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # Check Email
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        # Create User
        user = CustomUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone=phone,
            role=role,
            password=password
        )

        user.save()

        messages.success(request, "Registration Successful!")

        return redirect("login")

    return render(request, "accounts/register.html")


def user_login(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.role == "ADMIN":
                return redirect("admin_dashboard")

            elif user.role == "CUSTOMER":
                return redirect("customer_dashboard")

            elif user.role == "OWNER":
                return redirect("owner_dashboard")

            elif user.role == "DRIVER":
                return redirect("driver_dashboard")

            elif user.role == "PARTNER":
                return redirect("partner_dashboard")

        else:

            messages.error(request, "Invalid Username or Password")

    return render(request, "accounts/login.html")


def user_logout(request):

    logout(request)

    return redirect("home")