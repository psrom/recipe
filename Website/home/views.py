from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from django.http import HttpResponseNotFound
from regex import D # 404 error
from .models import Ingredient

from recipe_model import *

# Create your views here.
def index(request):
    print(request.user)
    return render(request, 'index.html')

def login(request):
    if request.method == "POST":
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        return render(request, 'signup.html')

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
    return HttpResponse(json.dumps({'result':result, 'jar':jar}), content_type="application/json")
    

    # return render(request, 'index.html', {'result':result, 'jar':round(jar,3), 'list':i})
