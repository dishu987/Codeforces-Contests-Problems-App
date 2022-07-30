from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
# add a flag for
# handling the 404 error
#handler404 = 'core.views.error_404_view'
handler500 = 'core.views.error_500_view'
handler404 = 'core.views.error_404_view'