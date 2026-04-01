from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from .settings import DEBUG, STATIC_URL, STATIC_ROOT, MEDIA_URL, STATICFILES_DIRS

urlpatterns = [
    path('admin/', admin.site.urls),
]

if DEBUG:
    urlpatterns += static(STATIC_URL,document_root = STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root = STATIC_ROOT)