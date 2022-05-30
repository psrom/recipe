from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from django.http import HttpResponseNotFound
from regex import D # 404 error
from .models import Ingredient
from .models import Home
from accounts.models import Hate_Ingredient
from recipe_model import *
import requests
from bs4 import BeautifulSoup

import random

# Create your views here.
def index(request):
    RECIPE_NUM=8
    
    rand_val = random.randint(0, 10000)


    default_recipe = Home.objects.filter().all()[rand_val:rand_val+RECIPE_NUM] # random 8개 
    return render(request, 'index.html', {"context": default_recipe})

    
def ingredientsjson(request):
    if not request.GET.get('ingredient'):
        ingredient = Ingredient.objects.all()
        # raise HttpResponseNotFound("Required ingredient")
    else:
        ingredient = Ingredient.objects.filter(ingredients__startswith=request.GET['ingredient']).all()

    return HttpResponse(serialize('json', queryset=ingredient))


import json

def rec(request):
   
    
    if not request.GET.get('ingre'):
        ingredient = Ingredient.objects.all()
        
    else:
        data = request.GET.get('ingre')
        data = data.split(',') # list
        jar, result = Ing_rec(data).rec()
        result_lst = []
        for i in result.values():
            for j in i:
                result_lst.append(j) 
        print(jar)
        print("-"*10)
        print(result)
        print(result_lst)
    return HttpResponse(json.dumps({'result':result, 'jar':round(jar,3)}), content_type="application/json")
    



def recipe_rec(request):
    print(request.user.id)
    id = Hate_Ingredient.objects.filter(user_id = request.user.id).values('ingredient_id')
    
    e = [Ingredient.objects.get(id = i['ingredient_id']) for i in id]
    
    hate = [i.ingredients for i in e]
    print(hate)

    lst = [i['value'] for i in eval(request.GET.get('input-custom-dropdown'))]
    print(lst)
    input_lst = Recipe_rec(lst)

    max_idx = input_lst.cosin_m(n = 500, p = True)
   
    max_idx_ing = [eval(Home.objects.get(id = i+1).ingredients_pre) for i in max_idx]
    
    print(len(max_idx))
    idx = [] 
    for i in hate:
        for j in range(len(max_idx_ing)):
            if i in max_idx_ing[j]:
                idx.append(j)
    idx = list(set(idx))            
    
    for index in sorted(idx, reverse=True):
        del max_idx[index]

    print(len(max_idx))            
    n10 = input_lst.rec_result(max_idx, n = 60)
    
    
    recc = [Home.objects.get(id = i+1) for i in n10]
    


    print(recc)
    print(recc[0].image_url)
               
    return render(request, 'index.html', {'context':recc, 'lst':lst, 'hate':hate})

