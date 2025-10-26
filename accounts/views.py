from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy

from accounts.forms import LoginForm


# Create your views here.
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