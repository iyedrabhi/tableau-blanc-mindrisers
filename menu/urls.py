from django.urls import path

from . import views

app_name = "menu"

urlpatterns = [
    path("", views.dish_list, name="dish_list"),
    path("landing/", views.landing, name="landing"),
    path("add/", views.dish_create, name="dish_create"),
    path("<int:pk>/edit/", views.dish_update, name="dish_update"),
    path("<int:pk>/delete/", views.dish_delete, name="dish_delete"),
]

