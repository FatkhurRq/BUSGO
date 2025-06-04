from django.urls import path
from . import views

app_name = 'bus'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_schedules, name='search_schedules'),
    path('<slug:operator_slug>/', views.operator_detail, name='operator_detail'),
    path('schedule/<int:schedule_id>/', views.ticket_detail, name='ticket_detail'),
    path('book/<int:schedule_id>/', views.book_ticket, name='book_ticket'),
    path('booking-success/<int:booking_id>/', views.booking_success, name='booking_success'),
]