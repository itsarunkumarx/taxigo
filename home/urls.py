from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("contact/", views.contact, name="contact"),
    path("googlee0d51be61ec8057d.html", views.google_verification),
    path("robots.txt", views.robots_txt),
    path("sitemap.xml", views.sitemap_xml),
]