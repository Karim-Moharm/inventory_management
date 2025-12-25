from django.urls import path
from .views import TemplateView, SignUpView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", TemplateView.as_view(), name="dashboard"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="inventory/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "logged-out/",
        TemplateView.as_view(template_name="inventory/logout.html"),
        name="logged_out",
    ),
]
