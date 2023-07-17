"""instagram_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = 'post.views.handler404'