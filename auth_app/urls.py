from django.urls import path

from auth_app.views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
]