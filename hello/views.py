from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import requests
from .models import Greeting
from .stella.stella import stella
from .stella.utils import MLStripper, ContentApi

# Create your views here.
def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print("hello")
    return HttpResponse('<pre>' + "Pure Belgium \n &#127866;" + '</pre>')


def predict(request):
    # try:
    url = request.GET.get('url', None)
    
    if url is not None:
        c = ContentApi(MLStripper)
        text = c.get_article_text(url)

        if text is None: return HttpResponse("Article not yet available for auto-tagging. \n Please make sure you have scheduled your article.", content_type='application/json')
    else:
        text = request.GET.get('text', None)

        if text is None: return HttpResponse("Check suggested tags by passing in article url using url param. Make sure the article is scheduled or published: \n   /stella/?url=www.whowhatwear.com/best-dressed-celebrities-2-17-18--5a8254a17230b \n\nCheck suggested tags by passing in text using text param: \n   /stella/?text=these top 10 jeans are amazing", content_type='application/json')
    
    

    stell = stella()
    data = stell.predict(text,.000001)
   
    print("Stella")

    return HttpResponse(data, content_type='application/json')
    

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

