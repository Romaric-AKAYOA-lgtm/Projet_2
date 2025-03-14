from django.urls import path
from .views import send_sms_api

app_name = 'Notifications'

urlpatterns = [
    path("send_sms/", send_sms_api, name="send_sms"),
]
