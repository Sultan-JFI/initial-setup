from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ایمپورت کردن نمونه CustomAdminSite که در news/admin.py تعریف کردیم
from news.admin import admin_site 

urlpatterns = [
    # جایگزینی admin.site پیش‌فرض با admin_site سفارشی ما
    path('admin/', admin_site.urls),
    
    path('', include('news.urls')), 
    # path('accounts/', include('accounts.urls')),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
