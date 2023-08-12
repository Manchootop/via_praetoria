import logging

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

print(settings.DEBUG)
print(settings.SECRET_KEY)

logger = logging.getLogger(__name__)
logger.debug('This is a test')
logger.info('This is from info')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('auth/', include('auth_app.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
