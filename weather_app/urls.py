from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from rest_api import views

# router = routers.DefaultRouter()
# router.register(r'weather', views.WeatherViewSet, basename='weather')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/', views.weather_list),
    path('weather/<int:pk>/', views.weather_detail)
]

urlpatterns = format_suffix_patterns(urlpatterns)
