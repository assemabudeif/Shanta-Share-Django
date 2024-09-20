
from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login),
    # path('client-login', views.client_login),

    path('client-register', views.ClientRegisterView.as_view()),

    # path('driver-login', views.driver_login),

    path('driver-register', views.DriverRegisterView.as_view()),

    # path('admin-login', views.admin_login),
    path('admin-register', views.admin_register),
]