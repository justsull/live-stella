from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import Greeting
from .stella.stella import stella
from .slack.slack_handler import CommandHandler
from .stella.utils import MLStripper, ContentApi

# Create your views here.
def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print("hello")
    return HttpResponse('<pre>' + "Pure Belgium \n &#127866;" + '</pre>')

@csrf_exempt
def predict(request):
    if request.method == 'GET':
        url = request.GET.get('url', None)
        text = request.GET.get('text', None)
    
    elif request.method == 'POST':
        url = request.POST.get('url', None)
    
    if url is not None:
        c = ContentApi(MLStripper)
        text = c.get_article_text(url)

        if text is None: return HttpResponse("Article not yet available for auto-tagging. \nPlease make sure you have scheduled your article.", content_type='application/json')

    stell = stella()
    data = stell.predict(text,.000001)
   
    print("stella")

    return JsonResponse(data, content_type='application/json')

@csrf_exempt
def slack_predict(request):
    post = request.POST
    slash_command = CommandHandler(post)
    url = slash_command.url
    
    if url is not None:
        c = ContentApi(MLStripper)
        text = c.get_article_text(url)

        if text is None: 
            data = "Article not yet available for auto-tagging. \nPlease make sure you have scheduled your article."
            message = slash_command.form_response(data) 
            return JsonResponse(message, content_type='application/json')

        stell = stella()
        data = stell.predict(text,.000001)
        message = slash_command.form_response(data) 

        return JsonResponse(message, content_type='application/json')
    
    return JsonResponse({'response': "Please make sure to provide an article url."}, content_type='application/json')
    

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

