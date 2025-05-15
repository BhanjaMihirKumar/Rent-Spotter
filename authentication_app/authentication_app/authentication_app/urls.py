# authentication_app/urls.py

from django.urls import path
from .views import home, register, user_login, land_lord, public_user_profile, about,search, contact

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('land_lord/', land_lord, name='land_lord'),
    path('public_user_profile/<str:username>/', public_user_profile, name='public_user_profile'),
    path('about/',about ,name='about'),
    path('contact',contact, name='contact'),
    path('search/', search, name='search'),
    # Add other URLs as needed
]
