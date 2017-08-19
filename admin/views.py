#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author: Abel Lee
#date: 2017
#Copyright: free

from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'static/ue.html')

def logout(request):
    return render(request, 'static/ue.html')

def index(request):
    return render(request, 'static/ue.html')


