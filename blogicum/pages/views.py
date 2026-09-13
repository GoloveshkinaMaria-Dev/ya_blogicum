from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "pages/about.html"


class RulesView(TemplateView):
    template_name = "pages/rules.html"


def page_not_found(request, exception):
    return render(request, "pages/404.html", status=404)


def permission_denied(request, exception):
    return render(request, "pages/403csrf.html", status=403)


def server_error(request):
    return render(request, "pages/500.html", status=500)


def registration(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")

    return render(request, "auth/registration.html", {"form": form})
