from django.urls import path
from .views import create_call_session, join_call_session

app_name = 'call'

urlpatterns = [
    path('create/', create_call_session, name='create_call'),
    path('join/', join_call_session, name='join_call'),
]
