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
from common.password import check_password

# Create your views here.

def index(request):
    try:
        log_error("---------admin_index")
        if request.session.get('username'):
            log_error("======session[username]=%s" % request.session.get('username'))
            return render(request, 'static/admin/admin.html', {"username": request.session.get('username')})
    except Exception,e:
        log_error("admin index Exception:%s" % e)

    return render(request, 'static/admin/login.html')

def login(request):
    try:
        log_debug('in login---method:%s' % request.method)
        if request.session.get('username'):
            log_error("======session[username]=%s" % request.session.get('username'))
            ret = return_success(data={'username': request.session.get('username')})
            return HttpResponse(json.dumps(ret))

        if request.method == 'POST':
            log_debug(request.body)
            form = json.loads(request.body)
            log_error("form:%s" % form)

            if form:
                username = form['username']
                password = form['password']
                log_error("username:%s, password:%s" % (username, password))

                userinfo = User.objects.filter(username=username)
                log_error("userinfo:%s" % userinfo)
                if userinfo == None or len(userinfo) != 1:
                    ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                             ErrMsg.ERR_MSG_INTERNAL_ERROR))
                    log_error("---ERR:%s" % ret)
                    return HttpResponse(json.dumps(ret))

                if check_password(password, userinfo[0].password):
                    log_error("---------password OK---session_key:%s" % str(request.session.session_key))
                    request.session.create()
                    request.session.save()
                    request.session['username'] = username
                    ret = return_success(data={"username": username})
                    return HttpResponse(json.dumps(ret))
                else:
                    log_error("---------password ERROR")
                    ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                             ErrMsg.ERR_MSG_LOGIN_ERROR),
                                       dict(username=username, password=password))

                    return HttpResponse(json.dumps(ret))
    except Exception,e:
        log_error('login with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))
        log_error("ERR:%s" % ret)
        return HttpResponse(json.dumps(ret))

def logout(request):
    try:
        if request.method == 'GET':
            username = request.GET['username']
            if username:
                del request.session[username]
        ret = return_success()
    except Exception,e:
        log_error('logout with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))
    return HttpResponse(json.dumps(ret))
