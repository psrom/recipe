from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from django.core.serializers import serialize
from django.http import HttpResponseNotFound
from regex import D # 404 error
from .models import Hate_Ingredient
from home.models import Ingredient
import json

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        if User.objects.filter(username=username).all():
            return render(request, 'signup.html', {"error": {"message":"중복된 아이디입니다."}})

        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"], password=request.POST["password1"])
            auth.login(request, user)
        else:
            return render(request, 'signup.html', {"error": {'message': "비밀번호가 일치하지 않습니다."}})
         
        #return render(request, 'signup_hate.html')
        #return redirect('signup_hate')
        return redirect('register_hate')
    return render(request, 'signup.html')



def register_hate(request):
    if request.user.is_authenticated:
        # 로그인 되어있는 사람만 접근 가능
        return render(request, 'signup_hate.html')
    else:
        # 로그인 안되어 있을 시에 login페이지로 redirect
        return redirect('login')



def signup_hate(request):
    if request.method == 'POST':
        data =  request.POST
        hate_ingredients = data.get('hate_ingredients')
        hate_ingredients = json.loads(hate_ingredients)
        ingrement_list = [item['value'] for item in hate_ingredients]
        target_ing_objs = Ingredient.objects.filter(ingredients__in=ingrement_list).all()

        
        hate_ingredients=[Hate_Ingredient(
            user=request.user,
            ingredient= ingre_obj
            ) for ingre_obj in target_ing_objs]
        Hate_Ingredient.objects.bulk_create(hate_ingredients)
    return redirect('index')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {"error":{"message":"아이디, 비밀번호를 다시 확인해주세요."}})
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')


def modify(request):
    if request.method == 'POST' or 'GET':
        return render(request, 'modify.html')



def ingredientsjson(request):
    if not request.GET.get('ingredient'):
        ingredient = Ingredient.objects.all()
        # raise HttpResponseNotFound("Required ingredient")
    else:
        ingredient = Ingredient.objects.filter(ingredients__startswith=request.GET['ingredient']).all()

    return HttpResponse(serialize('json', queryset=ingredient))
