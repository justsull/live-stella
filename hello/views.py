from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import Greeting
from .stella.stella import stella
from .slack.slack_handler import CommandHandler
from .stella.utils import MLStripper, ContentApi
from threading import Thread
import json

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
        method = request.GET.get('method', 'stella')
        size = int(request.GET.get('size', 1))
    
    elif request.method == 'POST':
        url = request.POST.get('url', None)
        method = request.POST.get('method', 'stella')
        size = int(request.POST.get('size', 1))
    
    if url is not None:
        c = ContentApi(MLStripper)
        _, text = c.get_article_text(url)

        if text is None: return HttpResponse("Article not yet available for auto-tagging. \nPlease make sure you have scheduled your article.", content_type='application/json')
    
    stell = stella()
    if method.lower() == 'fuzzy':
        data = stell.fuzzy_predict(text,size=size)
    else:
        data = stell.predict(text,.000000001)
   
    print("stella")

    return JsonResponse(data, content_type='application/json')

@csrf_exempt
def slack_predict(request):
    post = request.POST
    slash_command = CommandHandler(post)
    url = slash_command.url
    response_url = slash_command.response_url
    print("this is the url: {}".format(url))
    print("this is the response url: {}".format(response_url))

    thr = Thread(target=background_stella, args=[url,response_url])
    thr.start()

    string = "Analyzing your article: {}".format(url)

    message = {'text': string}

    return JsonResponse(message, content_type='application/json')


def background_stella(url, response_url):
    headers = {'Content-type': 'application/json'}

    if url is not None:
        c = ContentApi(MLStripper)
        _, text = c.get_article_text(url)
        print("this is the text from background_stella: {}".format(text))

        if text is None:
            data = "Article not yet available for auto-tagging. \nPlease make sure you have scheduled your article."
            message = CommandHandler.form_response(data) 

            requests.post(response_url,data=json.dumps(message), headers=headers)

        stell = stella()
        data = stell.predict(text,.000000001)
        message = CommandHandler.form_response(data) 

        r = requests.post(response_url,data=json.dumps(message),headers=headers)
    
    message = {'text':'Cheers! \n:beer:'}

    requests.post(response_url,data=json.dumps(message),headers=headers)

