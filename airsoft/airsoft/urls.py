"""airsoft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include("homepage.urls")),
    path("teams/", include("airsoft_teams.urls")),

    path('registration/', include("airsoft_registration.urls")),

    path('organization/', include("airsoft_organization.urls")),
    path('events/', include("airsoft_event.urls")),
    path('shops/', include("airsoft_shops.urls")),
    path("admin/", admin.site.urls),
    path('auth/', include("u_auth.urls")),


    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# admin if debug
if settings.DEBUG:
    urlpatterns.append(
        path('__debug__/', include('debug_toolbar.urls')),
    )
