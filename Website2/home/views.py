from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from django.http import HttpResponseNotFound
from regex import D # 404 error
from .models import Ingredient
from .models import Home
from recipe_model import *
import requests
from bs4 import BeautifulSoup

# Create your views here.
def index(request):
    #print(request.user)
    #Ingredient.objects.get().hate_users()
    #print(request.user.hate_ingredients.all())
    return render(request, 'index.html')

    
def ingredientsjson(request):
    if not request.GET.get('ingredient'):
        ingredient = Ingredient.objects.all()
        # raise HttpResponseNotFound("Required ingredient")
    else:
        ingredient = Ingredient.objects.filter(ingredients__startswith=request.GET['ingredient']).all()

    return HttpResponse(serialize('json', queryset=ingredient))

# def personToDictionary(person):
#     if person == None:
#         return None

#     dictionary = {}
#     dictionary["username"] = person.username
#     dictionary["firstName"] = person.firstName
#     dictionary["middleName"] = person.middleName
#     dictionary["lastName"] = person.lastName
#     dictionary["age"] = person.age

#     return dictionary

# person = Person.objects.get(id = 25)
# personDictionary = personToDictionary(person)

# from django.core import serializers

# person = serializers.serialize("json", Person.objects.get(id = 25))
# people = serializers.serialize("json", Person.objects.all())

# from django.core import serializers

# person = serializers.serialize("json", Person.objects.get(id = 25), fields = ("firstName", "middleName", "lastName"))
# people = serializers.serialize("json", Person.objects.all(), fields = ("firstName", "middleName", "lastName"))


import json

def rec(request):
    # k = request.GET.get('input-custom-dropdown')
    # i = [eval(k)[i]['value'].split(',') for i in range(len(eval(k)))]
    # i = sum(i, [])
    # print(eval(k))
    # print(len(eval(k)))
    # print(i)

    # jar, result = Ing_rec(i).rec()
    
    if not request.GET.get('ingre'):
        ingredient = Ingredient.objects.all()
        # raise HttpResponseNotFound("Required ingredient")
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
    

    # return render(request, 'index.html', {'result':result, 'jar':round(jar,3), 'list':i})






def recipe_rec(request):
    
    
    lst = [i['value'] for i in eval(request.GET.get('input-custom-dropdown'))]
    print(lst)
    input_lst = Recipe_rec(lst)

    max_idx = input_lst.cosin_m(n = 100, p = True)

    n10 = input_lst.rec_result(max_idx, n = 8)
    
    
    recc = [Home.objects.get(id = i+1) for i in n10]
    print(recc)
    
    url = [i.url for i in recc]
    image_url = []
    for i in url:
        res = requests.get(i)
        soup = BeautifulSoup(res.content, 'html.parser')


        if '10000recipe' in i:
            image = soup.find('div', 'centeredcrop').find('img')['src']
            image_url.append(image)
        elif 'haemukja' in i:
            if soup.find('div', 'flexslider') != None:

                image = soup.find('div', 'flexslider').find_all('img')[0]['src']
                image_url.append(image)
            else:    
                image = soup.find('ol','lst_step').find_all('div', 'img-cover')[-1].find('img')['src']
                image_url.append(image)    

        else:
            image = 'https://wtable.co.kr'+soup.find('div', style = "display:inline-block;max-width:100%;overflow:hidden;position:relative;box-sizing:border-box;margin:0").find_all('img')[1]['src']
            image_url.append(image)

    context = []
    for i in range(len(image_url)):
        dic = {}
        dic['name'] =recc[i].name
        dic['ingredients'] = recc[i].ingredients
        dic['url'] = recc[i].url
        dic['img_url'] = image_url[i]
        context.append(dic) 

    print(context)            
    return render(request, 'index.html', {'context':context, 'lst':lst})