from django.urls import path

from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('api/ingredient/', views.ingredientsjson, name='ingredient_json')
]