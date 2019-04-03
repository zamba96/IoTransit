from django.shortcuts import render
from django.http import HttpResponse
from . import streams
import json
from django.db import connections
import numpy as np
from datetime import datetime
from .Registro import Registro

# Create your views here.
global map

def index(request):
    map = streams.otherMain()
    a = ''
    for x, y in map.items():
        a += '{}:{}\n'.format(x, y)
    # return HttpResponse(a)
    print(map)
    return HttpResponse(json.dumps(map), content_type='application/json')


def voy(request, pk):
    template='base.html'
    datos=[]
    y=[]
    z=[]
    with connections['default2'].cursor() as cursor:
        cursor.execute("SELECT * FROM lecturas ")
        row = cursor.fetchone()

        print(type(row))

        while row is not None:
          print(row)
          datos.append(list(row))
          m= str(datetime.fromtimestamp(row[0]))
          y.append(m)
          print(type(row))

          row = cursor.fetchone()
        print("callo")
        inputs = np.array(datos)
        print(inputs[:,0])
        x=range(len(inputs))
        print(datetime.fromtimestamp(inputs[0,0]))
        va=list(inputs[:,int(pk)])
        cont=0
        for w in va:
            p= Registro(y[cont],pk,w)
            z.append(p)
            cont=cont+1
        context = {"categories": list(y), 'values': va, 'table_data':inputs, 'tamx':z}
    return render(request, template, context=context)
def sensores(request):
    template='basesenso.html'
    datos=[]
    z=[]
    x1=[]
    y1=[]
    tam=30
    with connections['default2'].cursor() as cursor:
        cursor.execute("SELECT * FROM lecturas ")
        row = cursor.fetchone()
        cont=0
        while row is not None:
          datos.append(list(row))
          m= str(datetime.fromtimestamp(row[0]))
          for x in range(1, len(row)):
              y= Registro(m,x,row[x])
              z.append(y)
              if(cont==0):
                  u=0
                  x1=range(len(row)-1)
                  x1=list(range(len(row)-1))

                  for t in row:
                      if(u!=0):
                          y1.append(t)
                      u=1
                  cont=cont+1

          row = cursor.fetchone()
        inputs = np.array(datos)
        tamx=[]
        for x in range(0, tam):
            tamx.append(z[x])
        context = {'query': datos, 'table_data':inputs, 'tam':tam, 'tamx':tamx, 'x1':x1,'y1':y1}
    return render(request, template, context=context)
