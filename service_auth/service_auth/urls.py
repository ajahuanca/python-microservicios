from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('auth/schema/', SpectacularAPIView.as_view(), name='auth-schema'),
    path('auth/docs/swagger/', SpectacularSwaggerView.as_view(url='/auth/schema/'), name='auth-swagger-ui'),
    path('auth/docs/redoc/', SpectacularRedocView.as_view(url='/auth/schema/'), name='auth-redoc'),
    path('auth/admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
]
