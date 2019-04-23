from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from ecomm import settings

urlpatterns = [
    path('api/v1/',include('social_django.urls',namespace='social')),
    path('admin/', admin.site.urls),
    path("", include('eco.urls')),





]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
