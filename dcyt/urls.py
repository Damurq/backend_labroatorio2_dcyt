from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/",include('rest_framework.urls')),
    path("api/",include('users.urls')),
    path("api/",include('pensum.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns += [re_path(r'ˆ.*', TemplateView.as_view(template_name='index.html'))]
