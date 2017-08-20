#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author: Abel Lee
#date: 2017
#Copyright: free

import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import User
from common.logger import log_error,log_info,log_debug
from common.error import return_error, return_success, Error
import common.err_msg as ErrMsg
import common.err_code as ErrCode

# Create your views here.

def index(request):
    return render(request, 'static/admin.html')

def login(request):
    try:
        if request.method == 'POST':
            form = json.loads(request.body)

            if form is not None:
                username = form['username']
                password = form['password']

                userinfo = User.objects.filter(username=username)
                if userinfo == None or len(userinfo) != 1:
                    return render(request, 'static/login.html')

                if username == userinfo[0].username and password == userinfo[0].password:
                    ret = return_success()
                else:
                    ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                             ErrMsg.ERR_MSG_LOGIN_ERROR),
                                       dict(username=username, password=password))

                response = HttpResponse(json.dumps(ret))
                if ret['status'] == 0:
                    response.set_cookie('username', username, 1800)
                return response
    except Exception,e:
        log_error('login Exception:%s' % e)
    ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                             ErrMsg.ERR_MSG_INTERNAL_ERROR))
    return HttpResponse(json.dumps(ret))

def logout(request):
    try:
        ret = return_success()
        response = HttpResponse(json.dumps(ret))
        response.delete_cookie('username')
    except:
        pass
    return response
