from importlib.metadata import pass_none
from urllib.parse import uses_relative

from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.template.defaulttags import autoescape
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from accounts.forms import LoginForm, PatientSignupForm


# Create your views here.

class LandingView(TemplateView):
    template_name = 'accounts/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        context['signup_form'] = PatientSignupForm()
        return context

class PatientSignupView(FormView):
    template_name = 'accounts/landing.html'
    form_class = PatientSignupForm
    success_url = reverse_lazy('patient:me')

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)

        try:
            role = user.role
            if role == user.Role.SYSADMIN:
                return redirect("admin:index")
            if role == user.Role.DOCTOR:
                return redirect("doctor-dashboard")
            if role == user.Role.STAFF:
                return redirect("appointments:list")
            if role == user.Role.STAFF:
                return redirect("patient:me")
        except Exception:
            pass

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        return context

class RoleLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        # Remember me handling
        remember = form.cleaned_data.get('remember_me')
        if remember:
            self.request.session.set_expiry(None)
        else:
            self.request.session.set_expiry(0)
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        default = reverse_lazy("dashboard")

        role = getattr(user, "role", None)
        if role:
            return default

        if role == user.Role.SYSADMIN:
            return reverse_lazy("admin:index")
        if role == user.Role.DOCTOR:
            return reverse_lazy("doctor-dashboard")
        if role == user.Role.STAFF:
            return reverse_lazy("appointments:list")
        if role == user.Role.PARTICIPANT:
            return reverse_lazy("patient:me")
        return default

class RoleLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")