from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import requests
from .models import Greeting
from .stella.stella import stella

# Create your views here.
def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print("hello")
    return HttpResponse('<pre>' + "Pure Belgium" + '</pre>')


def predict(request):
    text = request.GET.get('text', '')
    # percent = request.GET.get('percent', .03)
    stell = stella()
    data = stell.predict(text,.03) 
    print("Stella")
    return HttpResponse(data, content_type='application/json')

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

