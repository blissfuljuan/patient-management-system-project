from django.urls import path

from . import views

app_name = "appointments"

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='list'),
    path('book/<int:slot_id>', views.book_appointment, name='book'),

    path('<int:pk>/confirm', views.confirm_appointment, name='confirm'),
    path('<int:pk>/complete', views.complete_appointment, name='complete'),
    path('<int:pk>/cancel', views.cancel_appointment, name='cancel'),
    path('<int:pk>/no-show', views.no_show_appointment, name='no_show'),
]