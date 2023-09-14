from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from auth_app import views
from auth_app.views import CustomTokenObtainPairView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register user'),
    path('login/', views.LoginView.as_view(), name='login user'),
    path('logout/', views.LogoutView.as_view(), name='logout user'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

