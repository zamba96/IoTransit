from django.shortcuts import render
from django.http import HttpResponse
from . import streams
import json
from django.db import connections
import numpy as np
from datetime import datetime
from .Registro import Registro
import cv2
import sys
from EmoPy.src.fermodel import FERModel
from pkg_resources import resource_filename
import os
from PIL import Image, ImageDraw, ImageFont
global map

def index(request):
    template='index.html'
    map = streams.otherMain()
    a = ''
    for x, y in map.items():
        a += '{}:{}\n'.format(x, y)
    # return HttpResponse(a)
    print(map)
    #return HttpResponse(json.dumps(map), content_type='application/json')
    return render(request, template)


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
        print(len(z))
        if(len(z)>tam-1):
            for x in range(len(z)-tam-1, len(z)):
                tamx.append(z[x])
        context = {'query': datos, 'table_data':inputs, 'tam':tam, 'tamx':tamx, 'x1':x1,'y1':y1}
    return render(request, template, context=context)

def redNeuronal(request):
    template='basered.html'
    datos=[]
    z=[]
    x1=[]
    y1=[]
    tam=30
    with connections['default2'].cursor() as cursor:
        cursor.execute("SELECT * FROM pred ")
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
        print(len(z))
        if(len(z)>tam-1):
            for x in range(len(z)-tam-1, len(z)):
                tamx.append(z[x])
        context = {'query': datos, 'table_data':inputs, 'tam':tam, 'tamx':tamx, 'x1':x1,'y1':y1}
    return render(request, template, context=context)

def emopy(request):
    template='video.html'
    fontFace = cv2.FONT_HERSHEY_SIMPLEX;
    fontScale = 1;
    thickness = 2;

    #Specify the camera which you want to use. The default argument is '0'
    video_capture = cv2.VideoCapture(0)
    #Capturing a smaller image fçor speed purposes
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    video_capture.set(cv2.CAP_PROP_FPS, 15)

    #Can choose other target emotions from the emotion subset defined in fermodel.py in src directory. The function
    # defined as `def _check_emotion_set_is_supported(self):`
    target_emotions = ['happiness','disgust','surprise']
    model = FERModel(target_emotions, verbose=True)


    ret, frame = video_capture.read()
    r=os.path.dirname(os.path.abspath(__file__))
    r=r.replace("monitoring","IoTransit_web")
    file = r+'/static/image_data/image.jpg'
    cv2.imwrite(file,frame)

    frameString = model.predict(file)
    image = Image.open(file)
    draw = ImageDraw.Draw(image)
    # O bien /usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf.
    font = ImageFont.load_default()
    color = 'rgb(255, 255, 255)'
    draw.text((50, 50), frameString, font=font, fill="black")
    image.save(file)
    context = {'image': image, 'estado':frameString}
    return render(request, template, context=context)
