from django.shortcuts import render
from django.views.generic import TemplateView, View
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect


class TemplateView(TemplateView):
    template_name = "inventory/dashboard.html"


class SignUpView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "inventory/signup.html", {"form": form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, user)
            if login:
                return redirect("dashboard")
        return render(request, "inventory/signup.html", {"form": form})
