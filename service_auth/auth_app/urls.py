from django.urls import path
from .views import register, MyTokenObtainPairView


urlpatterns = [
    path('register/', register, name='register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]