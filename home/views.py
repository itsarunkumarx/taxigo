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

def google_verification(request):
    return render(request, "googlee0d51be61ec8057d.html")

def robots_txt(request):
    from django.http import HttpResponse
    content = "User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /dashboard/\nSitemap: https://rovexa.onrender.com/sitemap.xml\n"
    return HttpResponse(content, content_type="text/plain")

def sitemap_xml(request):
    from django.http import HttpResponse
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
</urlset>"""
    return HttpResponse(content, content_type="application/xml")