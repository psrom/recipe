from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.http import HttpResponseNotFound
from regex import D # 404 error
from .models import *
from home.models import *
import json

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        if not username:
            return render(request, 'signup.html', {"error": {"message":"아이디, 비밀번호를 입력해주세요."}})
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
        return redirect('accounts:register_hate')
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
        if not hate_ingredients:
            return redirect('index')
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
    if request.method == 'GET':
        # db에서 불러오기
        id = Hate_Ingredient.objects.filter(
            user_id=request.user.id).values('ingredient_id')
        e = [Ingredient.objects.get(id=i['ingredient_id']) for i in id]
        hate = [i.ingredients for i in e]
        return render(request, 'modify.html', {'hate': hate})

    if request.method == 'POST':
        # 삭제하기
        delete_ingre = Hate_Ingredient.objects.filter(user_id=request.user.id)
        delete_ingre.delete()
        # 추가하기
        data = request.POST
        hate_ingredients = data.get('hate_ingredients')
        hate_ingredients = json.loads(hate_ingredients)
        ingrement_list = [item['value'] for item in hate_ingredients]
        target_ing_objs = Ingredient.objects.filter(
            ingredients__in=ingrement_list).all()

        hate_ingredients = [Hate_Ingredient(
            user=request.user,
            ingredient=ingre_obj
        ) for ingre_obj in target_ing_objs]
        Hate_Ingredient.objects.bulk_create(hate_ingredients)
        return redirect('index')




def ingredientsjson(request):
    if not request.GET.get('ingredient'):
        ingredient = Ingredient.objects.all()
        # raise HttpResponseNotFound("Required ingredient")
    else:
        ingredient = Ingredient.objects.filter(ingredients__startswith=request.GET['ingredient']).all()

    return HttpResponse(serialize('json', queryset=ingredient))

def like_recipe(request, like_recipe_pk):
    
    print(request)
    print('-'*10)
    print(like_recipe_pk)
    if request.user.is_authenticated:
        # request.user = 현재 유저
        # like_recipe_pk = recipe id (Home)
        # 목적: Like_recipe 추가하는 것
        print(request.user)
        print(request.user.id)
        # 이미 좋아요가 눌려 있는지 (?) => Like_recipe에 ㅇrecipe_id와 user_id가 있는지
        like_recipe = Like_recipe.objects.filter(user=request.user, recipe_id=like_recipe_pk).all()
        print(like_recipe)
        if like_recipe:
            # 이미 좋아요 눌러져 있음
            # 좋아요 객체(Like_recipe에 Delete)
            #    like_recipe = Like_recipe.objects.filter(recipe_id=like_recipe_pk)
           like_recipe.delete()
           return HttpResponse(json.dumps({'recipe_id': like_recipe_pk, 'deleted': True}))
        else:
            like_recipe_objs = Home.objects.filter(id= like_recipe_pk).all()
            print(like_recipe_objs)
            print(Home.objects.all())
            print('-'*10)

            like_recipe=Like_recipe(user=request.user, recipe= like_recipe_objs[0])
            print(like_recipe)
            
            print('-'*10)
            Like_recipe.objects.bulk_create([like_recipe])
            # 좋아요가 눌려있지 않음
            # 좋아요 객체(Like_recipe에 Insert)
            print([like_recipe])
        return HttpResponse(serialize('json', queryset= [like_recipe]))
    return redirect('accounts:login')