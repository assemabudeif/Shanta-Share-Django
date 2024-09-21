from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, get_totals,get_annual_statistics
router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get_totals/', get_totals,name='get_totals'),
    path('get_annual_statistics/', get_annual_statistics,name='get_annual_statistics')
]