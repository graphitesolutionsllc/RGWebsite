from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='storis-home'),
    path('login/', views.login, name='storis-login'),
    path('singleUpdate/', views.singleUpdate, name='storis-singleupdate')
]