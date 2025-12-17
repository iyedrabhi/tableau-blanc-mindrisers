from django.urls import path
from . import views

urlpatterns = [
    path('', views.tables_list, name='tables_list'),
    path('tables_list/', views.tables_list, name='tables_list'),
]




