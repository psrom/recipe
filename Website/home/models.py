from django.db import models

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

    def __str__(self):
        return self.ingredients
    


