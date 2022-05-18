from django.db import models
class Home(models.Model):
    name = models.CharField(max_length = 100)
    ingredients = models.TextField()
    ingredients_pre = models.TextField()
    url = models.URLField()
    serving = models.IntegerField()
    cnt = models.IntegerField()
    cluster = models.IntegerField()

class Ingredient(models.Model):
    ingredients = models.TextField()