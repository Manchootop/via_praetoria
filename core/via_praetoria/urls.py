from django.contrib import admin
from django.urls import path, include
from django.conf import settings

print(settings.DEBUG)
print(settings.SECRET_KEY)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('auth/', include('auth_app.urls')),

]
