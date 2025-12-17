"""
URL configuration for gestiondescommandes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
import os
from django.shortcuts import redirect
urlpatterns = [
    path('admin/', admin.site.urls),
    path('commandes/', include('CommandesApp.urls')),
]

def redirect_404(request, exception=None):
    return redirect('/commandes/commandes_list/')   # <-- your target URL

handler404 = redirect_404
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    urlpatterns += static("/qr_codes/", document_root=os.path.join(settings.BASE_DIR, "gestiondescommandes/qr_codes"))


