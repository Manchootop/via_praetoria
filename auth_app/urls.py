from django.urls import path

from auth_app import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register user'),
    path('login/', views.LoginView.as_view(), name='login user'),
    path('logout', views.LogoutView.as_view(), name='logout user'),
]
