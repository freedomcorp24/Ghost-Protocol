from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('view/<int:ticket_id>/', views.view_ticket, name='view_ticket'),
    path('close/<int:ticket_id>/', views.close_ticket, name='close_ticket'),
    path('reopen/<int:ticket_id>/', views.reopen_ticket, name='reopen_ticket'),
    path('delete/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
    path('reply/<int:ticket_id>/', views.staff_reply, name='staff_reply'),
    path('escalate/<int:ticket_id>/', views.escalate_ticket, name='escalate_ticket'),
]
