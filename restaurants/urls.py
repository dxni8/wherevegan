from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurant_add', views.restaurant_add, name="restaurant_add"),
    path('gps_berechnen', views.gps_berechnen, name='gps_berechnen'),
    path('ip_location', views.einzel_standort_berechnen, name="ip_location"),
    path('recipes', views.recipes, name="recipes"),
    path('contact', views.contact, name='contact'),
    path('privacy', views.privacy, name='privacy'),
    path('phone_code', views.phone_code_view, name='phone_code'),
    path('email_again_view', views.email_again_view, name='email_again_view'),
    path('email_again', views.email_again, name='email_again'),
]