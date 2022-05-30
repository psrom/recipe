from unicodedata import category
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
    image_url = models.URLField()
    tag = models.TextField()
    category = models.TextField()
    bak = models.TextField()
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    ingredients = models.TextField()

    hate_users = models.ManyToManyField(User, related_name='hate_ingredients', through='accounts.Hate_Ingredient')
    def __str__(self):
        return self.ingredients