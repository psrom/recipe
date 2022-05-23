from django.db import models
from django.contrib.auth.models import User

class Home(models.Model):
    name = models.CharField(max_length = 100)
    ingredients = models.TextField()
    ingredients_pre = models.TextField()
    url = models.URLField()
    serving = models.IntegerField()
    cnt = models.IntegerField()
    cluster = models.IntegerField()
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    ingredients = models.TextField()

    hate_users = models.ManyToManyField(User, related_name='hate_ingredients', through='accounts.Hate_Ingredient')
    def __str__(self):
        return self.ingredients