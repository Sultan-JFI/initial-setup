from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')), # <-- Include news app URLs
    # path('accounts/', include('accounts.urls')), # Uncomment if you add accounts URLs later
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))] # Uncomment if using django-browser-reload