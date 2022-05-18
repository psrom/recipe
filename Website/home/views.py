from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from django.http import HttpResponseNotFound
from regex import D # 404 error
from .models import Ingredient

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