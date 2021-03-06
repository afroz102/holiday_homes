import debug_toolbar
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bookings.urls')),
    path('', include('home.urls')),
    path('', include('landlords.urls')),
    path('', include('tasks.urls')),
    path('', include('units.urls')),
    path('', include('users.urls')),

    path('__debug__/', include(debug_toolbar.urls)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
