from django.db import models
from django.contrib.auth.models import User
from home.models import Home
from home.models import Ingredient as HomeIngredient


class Hate_Ingredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user_id = models.IntegerField()
    ingredient=models.ForeignKey(HomeIngredient, on_delete=models.CASCADE)
    # ingredients = models.TextField()
    
class Like_recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Home, on_delete=models.CASCADE)