from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/', include('api_basic.urls')),
                  path('api/', include('order.urls')),
                  path('api-auth/login/', include('rest_framework.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
