from django.urls import path

from . import views

app_name = "appointments"

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='list'),
    path('book/<int:slot_id>/', views.book_appointment, name='book'),
]