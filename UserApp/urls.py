from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import logout_view

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.RoleLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('client/home/', views.client_home, name='client_home'),
    path('livreur/home/', views.livreur_home, name='livreur_home'),
    # Gerant Dashboard
    path('gerant/dashboard/', views.gerant_dashboard, name='gerant_dashboard'),
    
    # Clients Management
    # Clients Management
    # Clients Management
    path('gerant/clients/export/', views.export_clients_excel, name='export_clients_excel'),
    path('gerant/clients/create/', views.client_create, name='client_create'),  # <-- specific first
    path('gerant/clients/<str:pk>/', views.client_detail, name='client_detail'),  # <-- generic after
    path('gerant/clients/<str:pk>/update/', views.client_update, name='client_update'),
    path('gerant/clients/<str:pk>/delete/', views.client_delete, name='client_delete'),
    path('gerant/clients/<str:pk>/toggle-active/', views.client_toggle_active, name='client_toggle_active'),
    path('gerant/clients/', views.clients_list, name='clients_list'),  # <-- list last
    path('gerant/clients/export/', views.export_clients_excel, name='export_clients_excel'),


    
    # Livreurs Management
    # Livreurs Management
    path('gerant/livreurs/create/', views.livreur_create, name='livreur_create'),  # <-- put first
    # Export must be BEFORE generic <pk> to avoid matching
    path('gerant/livreurs/export/', views.export_livreurs_excel, name='export_livreurs_excel'),
    path('gerant/livreurs/<str:pk>/update/', views.livreur_update, name='livreur_update'),
    path('gerant/livreurs/<str:pk>/delete/', views.livreur_delete, name='livreur_delete'),
    path('gerant/livreurs/<str:pk>/toggle-active/', views.livreur_toggle_active, name='livreur_toggle_active'),
    path('gerant/livreurs/<str:pk>/', views.livreur_detail, name='livreur_detail'),  # <-- generic last
    path('gerant/livreurs/', views.livreurs_list, name='livreurs_list'),
    path('client/delete-account/', views.client_delete_own_account, name='client_delete_own'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)