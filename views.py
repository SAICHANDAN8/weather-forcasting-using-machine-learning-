from django.shortcuts import render
from django.http import HttpResponse
from collections import defaultdict
from .models import *
from .forms import *
from io import TextIOWrapper
from django.contrib import messages
from django_pandas.io import read_frame
import warnings
warnings.filterwarnings(action='once')
import os
import numpy as np
import pandas as pd
import random
import re
from urllib.parse import urlparse
import os.path
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from urllib.parse import urlparse
from tld import get_tld
from googlesearch import search
import warnings
warnings.simplefilter("ignore")
from datetime import datetime, date
import calendar
import holidays
from sklearn.tree import DecisionTreeRegressor
# Create your views here.
global loaded_model,data_img

def adminlogin1(request):
    return render(request, "adminlogin.html")

def adminloginentered(request):
    if request.method == 'POST':
        uname=request.POST['uname']
        passwd=request.POST['upasswd']
        if uname =='admin' and passwd =='admin':
            return render(request,"adminloginentered.html")
        else:
            return HttpResponse("invalied credentials")
    return render(request, "adminloginentered.html")

def userdetails(request):
    qs=userModel.objects.all()
    return render(request,"userdetails.html",{"qs":qs})

def activateuser(request):
    if request.method =='GET':
        uname=request.GET.get('pid')
        print(uname)
        status='Activated'
        print("pid=",uname,"status=",status)
        userModel.objects.filter(id=uname).update(status=status)
        qs=userModel.objects.all()
        return render(request,"userdetails.html",{"qs":qs})

# Create your views here.
def index(request):
    return render(request,'index.html')

def logout(request):
    return render(request, "index.html")

def userlogin(request):
    return render(request,'userlogin.html')

def userregister(request):
    if request.method=='POST':
        form1=userForm(request.POST)
        if form1.is_valid():
            form1.save()
            print("succesfully saved the data")
            return render(request, "userlogin.html")
        else:
            print("form not valied")
            return HttpResponse("form not valid")
    else:
        form=userForm()
        return render(request,"userregister.html",{"form":form})

def userlogincheck(request):
    if request.method == 'POST':
        sname = request.POST['email']
        print(sname)
        spasswd = request.POST['upasswd']
        print(spasswd)
        try:
            check = userModel.objects.get(email=sname,passwd=spasswd)
            print(check)
            status = check.status
            print('status',status)
            if status == "Activated":
                request.session['email'] = check.email
                return render(request, 'userpage.html')
            else:
                messages.success(request,'user is not activated')
                return render(request, 'userlogin.html')
        except Exception as e:
            print('Exception is ',str(e))
            pass
        messages.success(request,'Invalid name and password')
        return render(request,'userlogin.html')
    

filename = 'model/gradient_booster.sav'
model_predict = pickle.load(open(filename, 'rb'))


def checkspam(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        latitude=float(latitude)
        longitude = request.POST.get('longitude')
        longitude=float(longitude)
        wind_kph = request.POST.get('wind_kph')
        wind_kph=float(wind_kph)
        wind_degree = request.POST.get('wind_degree')
        wind_degree=int(wind_degree)
        pressure_mb = request.POST.get('pressure_mb')
        pressure_mb=float(pressure_mb)
        precip_in = request.POST.get('precip_in')
        precip_in=float(precip_in)
        humidity = request.POST.get('humidity')
        humidity=float(humidity)
        cloud = request.POST.get('cloud')
        cloud=float(cloud)        
        d = {'latitude':[latitude],'longitude':[longitude],'wind_kph':[wind_kph],'wind_degree':[wind_degree],'pressure_mb':[pressure_mb],
      'precip_in':[precip_in],'humidity':[humidity],'cloud':[cloud]}
        df = pd.DataFrame(d)
        result=model_predict.predict(df)
        print(result)
        return render(request, 'spamreport.html', {"object": latitude,"object1": longitude,"object2": wind_kph,"object3": wind_degree,"object4": pressure_mb,"object5": precip_in,"object6": humidity,"object7": cloud,"object8": round(result[0],2)})
    return render(request, 'spaminput.html')
        
def adddata(request):
    return render(request,'spaminput.html')
