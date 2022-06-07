from django.urls import path

from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('api/ingredient/', views.ingredientsjson, name='ingredient_json'),
    path('ing_rec/', views.rec, name = 'ingre'),
    path('recipe_rec/', views.recipe_rec, name = 'input-custom-dropdown'),
  
]