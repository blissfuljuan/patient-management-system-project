from django.urls import path

from . import views

app_name = "doctors"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("list/", views.DoctorListView.as_view(), name="list"),
    path("<int:pk>/", views.DoctorDetailView.as_view(), name="detail"),
]