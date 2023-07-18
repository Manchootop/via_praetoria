from django.urls import path

from main.views import Demo

print('hit')
urlpatterns = [
    path('', Demo.as_view(), name='dashboard')
]