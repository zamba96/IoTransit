from django.shortcuts import render
from django.http import HttpResponse
from . import streams
import json
# Create your views here.


def index(request):
    map = streams.otherMain()
    a = ''
    for x, y in map.items():
        a += '{}:{}\n'.format(x, y)
    # return HttpResponse(a)
    return HttpResponse(json.dumps(map), content_type='application/json')
