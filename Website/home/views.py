from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from django.http import HttpResponseNotFound
from regex import D # 404 error
from .models import Ingredient
from .models import Home
from accounts.models import Hate_Ingredient
from recipe_model import *


import random

# Create your views here.
def index(request):
    # db에서 불러오기
    id = Hate_Ingredient.objects.filter(
        user_id=request.user.id).values('ingredient_id')
    e = [Ingredient.objects.get(id=i['ingredient_id']) for i in id]
    hate = [i.ingredients for i in e]

    # 랜덤 레시피
    RECIPE_NUM = 8
    rand_val = random.randint(0, 10000)

    default_recipe = Home.objects.filter().all(
    )[rand_val:rand_val+RECIPE_NUM]  # random 8개
    return render(request, 'index.html', {"context": default_recipe, 'hate': hate})

    
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

    max_idx = input_lst.cosin_m(n = 400, p = True)
   
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
    n10 = input_lst.rec_result(max_idx, n = 40)
    


    new_dic = {i:dic[i] for i in n10}

    categories = list(set([dic[i] for i in n10]))
    ex_idx = categories.index('기타')
    categories[-1], categories[ex_idx] = categories[ex_idx], categories[-1] 
    print(categories)

    dic2 = {i :[] for i in categories}
    
    for i in new_dic.keys():
      for j in categories:
        if new_dic[i] ==j:
          dic2[j].append(i)

      

    for j in dic2.keys():
        nn = dic2[j] 
        recc = [Home.objects.get(id = i+1) for i in nn]
        
        sor = {}
        for i in range(len(recc)):
            sor[i] = len(recc[i].ingredients_pre.split(','))

        idxx = sorted(sor, key= lambda x : sor[x])

        
    
        recc = [recc[i] for i in idxx]
       
        
        dic2[j] = recc       

   
    recc = [Home.objects.get(id = i+1) for i in n10]
    
    sor = {}
    for i in range(len(recc)):
        sor[i] = len(recc[i].ingredients_pre.split(','))
    idxx = sorted(sor, key= lambda x : sor[x])
    print(idxx)

    recc_sort = [recc[i] for i in idxx]
   
    
   
    print(dic2)
    all = {'all':'all'}
    all_sort = {'all_sort': 'all_sort'}
    return render(request, 'index.html', {'context_sort': recc_sort, 'context':recc, 'idxx':idxx, 'lst':lst, 'hate':hate, 'cate_recipe': dic2, 'all':all, 'all_sort':all_sort})
