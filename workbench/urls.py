
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings


# from core import views as core_views
# from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('account.urls', namespace='account')),

    path('book', include('core.urls', namespace='core')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# handler404 = core_views.error_404
# handler500 = core_views.error_500