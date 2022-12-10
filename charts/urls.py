# INF601 - Advanced Programming in Python
# James Kobell
# Final Project
from django.urls import include, path

from . import views

# register url and create function before use
urlpatterns = [    
    path('', views.index, name='index'),   
    path('login_request/', views.login_request, name='login_request'),
    path('register/', views.register, name='register'),
    path('logout_request/', views.logout_request, name='logout_request'),
]