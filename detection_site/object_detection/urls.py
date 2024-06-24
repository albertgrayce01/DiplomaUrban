from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from detection.views import upload_image, view_results

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', upload_image, name='upload_image'),
    path('results/<int:pk>/', view_results, name='results'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
