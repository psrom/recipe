from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('modify/', views.modify, name='modify'),
    path('register_hate/', views.register_hate, name= 'register_hate'),
    path('register_hate/accounts/signup_hate/', views.signup_hate, name = 'signup_hate'),
    
]