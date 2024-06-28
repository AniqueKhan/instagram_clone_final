from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
import app_authentication

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app_authentication.urls')),
    path('',include('direct.urls')),
    path('',include("post.urls")),
    path('',include("notification.urls")),
    path('',include("stories.urls")),
    path('password_change',app_authentication.views.password_change,name='password_change'),
    path('password_change/done', app_authentication.views.password_change_done, name='password_change_done'),
    path("__debug__/", include("debug_toolbar.urls"))
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = 'post.views.handler404'