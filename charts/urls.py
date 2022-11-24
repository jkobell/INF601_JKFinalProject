# INF601 - Advanced Programming in Python
# James Kobell
# Mini Project 4
from django.urls import include, path

from . import views

# register url and create function before use
urlpatterns = [    
    path('', views.index, name='index'),
    path('exchange/', views.exchange, name='exchange'),
    path('currency/', views.currency, name='currency'),
    path('ticker/', views.ticker, name='ticker'),
    path('exchange/<int:exchange_id>/', views.exchange_detail, name='exchange_detail'),
    path('currency/<int:currency_id>/', views.currency_detail, name='currency_detail'),
    path('ticker/<int:ticker_id>/', views.ticker_detail, name='ticker_detail'),    
    path('login_request/', views.login_request, name='login_request'),
    path('register/', views.register, name='register'),
    path('logout_request/', views.logout_request, name='logout_request'),
]