from django.db import models
from django.contrib.auth.models import User

from home.models import Ingredient as HomeIngredient


class Hate_Ingredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user_id = models.IntegerField()
    ingredient=models.ForeignKey(HomeIngredient, on_delete=models.CASCADE)
    # ingredients = models.TextField()
    def __str__(self):
        return self.Hate_Ingredient
