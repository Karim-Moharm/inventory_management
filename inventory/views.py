from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from .forms import UserRegistrationForm, ItemForm
from django.contrib.auth import authenticate, login
from .models import InventoryItem, Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class Index(TemplateView):
    template_name = "inventory/index.html"


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        items = InventoryItem.objects.filter(created_by=request.user.id).order_by("pk")
        return render(request, "inventory/dashboard.html", {"items": items})


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


class ItemCreate(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = ItemForm
    template_name = "inventory/items_form.html"
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["help_text"] = "all fields marked * are required"
        return context

    def form_valid(self, form):
        """set created_by to the loggedin user"""
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = ItemForm
    success_url = reverse_lazy("dashboard")
    template_name = "inventory/items_form.html"
    slug_field = "sku"
    slug_url_kwarg = "sku"


class ItemDelete(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    success_url = reverse_lazy("dashboard")
    slug_field = "sku"
    slug_url_kwarg = "sku"
