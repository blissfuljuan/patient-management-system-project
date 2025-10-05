from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.PatientListView.as_view(), name='list'),
    path('new/', views.PatientCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.PatientUpdateView.as_view(), name='edit'),
]