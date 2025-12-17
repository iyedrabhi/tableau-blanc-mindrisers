from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from reservations.views_gerant import tables_list as gerant_tables_list
from reservations.views import simple_login, simple_logout
from . import view as project_view

# Rediriger la racine vers le login
def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('', redirect_to_login),  # redirige la racine vers /login/
    path('admin/', admin.site.urls),
    path('tables/', include('tables.urls')),
    path('gerant/', gerant_tables_list, name='gerant'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('reservations/', include('reservations.urls')),
    path('login/', simple_login, name='login'),
    path('logout/', simple_logout, name='logout'),
    path('test-notifs/', project_view.test_notifications, name='test_notifications'),
]
