from django.urls import path
from .views import home,login,register
urlpatterns = [
    path('',home, name = 'home'),
    path('check/in/',login, name = 'login'),
    path('account/',register, name = 'register'),
]
