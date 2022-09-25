from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>',
         views.order_history, name='order_history'),
    # Support model related
    path('support/', views.display_tickets,
         name='open-support-tickets'),
    path('add-ticket/', views.add_support_ticket,
         name='add-support-ticket'),
    path('toggle-ticket-status/<ticket_id>/',
         views.toggle_ticket_status, name='toggle-ticket-status'),
    path('ticket-details/<ticket_id>/', views.ticket_details,
         name='ticket-details'),
]
