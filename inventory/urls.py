from django.urls import path
from .views import TemplateView, SignUpView

urlpatterns = [
    path("", TemplateView.as_view(), name="dashboard"),
    path("signup/", SignUpView.as_view(), name="sign_up"),
]
