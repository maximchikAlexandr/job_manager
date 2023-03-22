from django.urls import path

from continuos_delivery.views import Webhook

urlpatterns = [
    path('update_server', Webhook.as_view(), name="update_server"),
]
