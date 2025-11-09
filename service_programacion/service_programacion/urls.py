from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('programacion/schema/', SpectacularAPIView.as_view(), name='programacion-schema'),
    path('programacion/docs/swagger/', SpectacularSwaggerView.as_view(url='/programacion/schema/'), name='programacion-swagger-ui'),
    path('programacion/docs/redoc/', SpectacularRedocView.as_view(url_name='/programacion/schema/'), name='programacion-redoc'),
    path('programacion/admin/', admin.site.urls),
    path('programacion/', include('app_c.urls')),
]
