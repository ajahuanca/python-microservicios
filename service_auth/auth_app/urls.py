from django.urls import path
from .views import RegisterView, MyTokenObtainPairView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]