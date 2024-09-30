from django.urls import path, include
from .views import generate_iframe, payment_callback, pay_now

urlpatterns = [
    path("iframe", generate_iframe),
    path("callback/", payment_callback, name="payment_callback"),
    path("pay-now", pay_now),
]
