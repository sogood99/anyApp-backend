from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('accounts.urls')),
    path('api/tweet/', include('tweets.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
