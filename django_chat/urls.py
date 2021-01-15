import server_config

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.root, name='root'),
    path('api/v1/', include('api.urls')),
    path('chat/', include('chat.urls')),
    path('users/', include('users.urls')),
    path('test/', views.hello_jasmine, name='hello_jasmine'),
]

if server_config.SERVER_NAME == 'dev':
    urlpatterns += \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
