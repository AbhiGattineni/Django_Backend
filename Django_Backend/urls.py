
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('backend_api.urls')),
    path('', include('transaction_api.urls')),
    path('api/', include('ml_api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)