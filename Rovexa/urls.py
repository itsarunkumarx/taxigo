"""
URL configuration for Rovexa project.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.conf.urls.static import static


# ─── Healthcheck ─────────────────────────────────────────────────────────────
def healthcheck(request):
    return JsonResponse({"status": "healthy", "service": "Taxigo/Rovexa", "uptime": "active"}, status=200)


# ─── Custom Error Handlers (V-01 fix: no debug tracebacks in production) ─────
def handler400(request, exception=None):
    """Bad Request"""
    return HttpResponse(
        "<h1>400 - Bad Request</h1><p>The server could not understand your request.</p>",
        status=400, content_type="text/html"
    )

def handler403(request, exception=None):
    """Forbidden / Rate Limited"""
    return HttpResponse(
        "<h1>403 - Access Denied</h1><p>You do not have permission to view this page. "
        "If you made too many requests, please wait a moment and try again.</p>"
        "<p><a href='/'>Return to Home</a></p>",
        status=403, content_type="text/html"
    )

def handler404(request, exception=None):
    """Not Found - clean page, no debug trace"""
    return HttpResponse(
        "<h1>404 - Page Not Found</h1><p>The page you requested could not be found.</p>"
        "<p><a href='/'>Return to Home</a></p>",
        status=404, content_type="text/html"
    )

def robots_txt(request):
    content = "User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /dashboard/\nSitemap: https://rovexa.onrender.com/sitemap.xml\n"
    return HttpResponse(content, content_type="text/plain")

def sitemap_xml(request):
    content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://rovexa.onrender.com/</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://rovexa.onrender.com/about/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://rovexa.onrender.com/contact/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://rovexa.onrender.com/booking/add/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>"""
    return HttpResponse(content, content_type="application/xml")


urlpatterns = [
    path("robots.txt", robots_txt),
    path("sitemap.xml", sitemap_xml),
    path("healthz", healthcheck, name="healthcheck"),
    path("healthz/", healthcheck),
    path("ping/", healthcheck, name="ping"),
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("", include("accounts.urls")),
    path("", include("requests_app.urls")),
    path("customer/", include("customer.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("vehicle/", include("vehicle.urls")),
    path("booking/", include("booking.urls")),
    path("payment/", include("payment.urls")),
    path("realtime/", include("realtime.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
