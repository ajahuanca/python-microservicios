from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('proyectos/schema/', SpectacularAPIView.as_view(), name='proyectos-schema'),
    path('proyectos/docs/swagger/', SpectacularSwaggerView.as_view(url='/proyectos/schema/'), name='proyectos-swagger-ui'),
    path('proyectos/docs/redoc/', SpectacularRedocView.as_view(url='/proyectos/schema/'), name='proyectos-redoc'),
    path('proyectos/admin/', admin.site.urls),
    path('proyectos/', include('app_b.urls')),
]