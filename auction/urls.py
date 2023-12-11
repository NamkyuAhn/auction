from django.conf.urls.static import static
from auction import settings
from django.urls import path, include

urlpatterns = [
    path('main', include('main.urls')),
    path('accounts', include('accounts.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
