from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('empresas/schema/', SpectacularAPIView.as_view(), name='empresas-schema'),
    path('empresas/docs/swagger/', SpectacularSwaggerView.as_view(url='/empresas/schema/'), name='empresas-swagger-ui'),
    path('empresas/docs/redoc/', SpectacularRedocView.as_view(url='/empresas/schema/'), name='empresas-redoc'),
    path('empresas/admin/', admin.site.urls),
    path('empresas/', include('app_a.urls')),
]