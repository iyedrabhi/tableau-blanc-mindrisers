# stock/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="stock/login.html"), name="login"),  # ✅ vraie vue login
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("stocks/", views.stock_list, name="stock_list"),
    path("stocks/create/", views.stock_create, name="stock_create"),
    path("stocks/<int:id>/update/", views.stock_update, name="stock_update"),
    path("stocks/<int:id>/delete/", views.stock_delete, name="stock_delete"),
    path("order/create/", views.create_order, name="create_order"),
]
