#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author: Abel Lee
#date: 2017
#Copyright: free

import json
import uuid
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core import serializers
from .models import User
from .models import Article
from .models import ArticleType
from .models import ArticleComment
from common.logger import log_error,log_info,log_debug
from common.error import return_error, return_success, Error
import common.err_msg as ErrMsg
import common.err_code as ErrCode
from common.password import check_password
import common.constants as const

# Create your views here.

def index(request):
    try:
        if request.session.get('username'):
            return render(request, 'static/admin/admin.html', {"username": request.session.get('username')})
    except Exception,e:
        log_error("admin index Exception:%s" % e)

    return render(request, 'static/admin/login.html')

def login(request):
    try:
        if request.session.get('username'):
            ret = return_success(data={'username': request.session.get('username')})
            return HttpResponse(json.dumps(ret))

        if request.method == 'POST':
            log_debug(request.body)
            form = json.loads(request.body)

            if form:
                username = form['username']
                password = form['password']

                userinfo = User.objects.filter(username=username)
                if userinfo == None or len(userinfo) != 1:
                    ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                             ErrMsg.ERR_MSG_INTERNAL_ERROR))
                    return HttpResponse(json.dumps(ret))

                if check_password(password, userinfo[0].password):
                    request.session.create()
                    request.session.save()
                    request.session['username'] = username
                    ret = return_success(data={"username": username})
                    return HttpResponse(json.dumps(ret))
                else:
                    ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                             ErrMsg.ERR_MSG_LOGIN_ERROR),
                                       dict(username=username, password=password))

                    return HttpResponse(json.dumps(ret))
    except Exception,e:
        log_error('login with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))
        return HttpResponse(json.dumps(ret))

def logout(request):
    try:
        if request.method == 'GET':
            username = request.GET['username']
            if username == request.session.get('username', ''):
                del request.session['username']

        ret = return_success()
    except Exception,e:
        log_error('logout with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))

    return HttpResponse(json.dumps(ret))

def getArticleType(request):
    try:
        if request.method == 'GET':
            articleTypes = ArticleType.objects.filter()
            log_error("======articleTypes:%s" % articleTypes)
            if articleTypes == None:
                ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                         ErrMsg.ERR_MSG_INTERNAL_ERROR))
                return HttpResponse(json.dumps(ret))

            data = []
            for item in articleTypes:
                arcType = {}
                arcType['type_id'] = item.type_id
                arcType['type_name'] = item.type_name
                arcType['description'] = item.description
                data.append(arcType)
            log_error('-----data: %s' % data)
            ret = return_success(data=data)
        else:
            ret = return_error(Error(ErrCode.ERR_CODE_INVALID_REQUEST_PARAM,
                                     ErrMsg.ERR_MSG_INVALID_REQUEST_PARAM))
    except Exception,e:
        log_error('getArticleType with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))

    return HttpResponse(json.dumps(ret))

def getArticleComment(request):
    try:
        if request.method == 'GET':
            ArticleComments = ArticleComment.objects.filter()
            log_error("======ArticleComments:%s" % ArticleComments)
            if ArticleComments == None:
                ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                         ErrMsg.ERR_MSG_INTERNAL_ERROR))
                return HttpResponse(json.dumps(ret))

            ret = return_success(data=ArticleComments)
        else:
            ret = return_error(Error(ErrCode.ERR_CODE_INVALID_REQUEST_PARAM,
                                     ErrMsg.ERR_MSG_INVALID_REQUEST_PARAM))
    except Exception,e:
        log_error('getArticleComment with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))

    return HttpResponse(json.dumps(ret))

def addArticle(request):
    try:
        log_debug('in addArticle---method:%s' % request.method)
        if not request.session.get('username', None):
            log_error("======user not login")
            ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                     ErrMsg.ERR_MSG_USER_NOT_LOGIN_ERROR))
            return HttpResponse(json.dumps(ret))

        if request.method == 'POST':
            log_debug(request.body)
            form = json.loads(request.body)
            log_error("form:%s" % form)

            if form:
                userinfo = User.objects.filter(username=form['auther'])
                if userinfo == None or len(userinfo) != 1:
                    ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                             ErrMsg.ERR_MSG_INTERNAL_ERROR))
                    log_error("---ERR:%s" % ret)
                    return HttpResponse(json.dumps(ret))
                if userinfo[0].role == const.USER_ROLE_ADMIN:
                    status = const.ATRICLE_STATUS_PUBLISH
                elif userinfo[0].role == const.USER_ROLE_NORMAL:
                    status = const.ATRICLE_STATUS_PREPARED
                else:
                    ret = return_error(Error(ErrCode.ERR_CODE_INVALID_REQUEST_PARAM,
                                             ErrMsg.ERR_MSG_INVALID_REQUEST_PARAM))
                    return HttpResponse(json.dumps(ret))


                Article.objects.create(article_id = uuid.uuid1(), title = form['title'],
                                       type_id=form['type_id'], auther = form['auther'],
                                       status=status, htlm_context = form['htlm_context'])

                ret = return_success()
                return HttpResponse(json.dumps(ret))
    except Exception,e:
        log_error('addArticle with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))
        log_error("ERR:%s" % ret)
        return HttpResponse(json.dumps(ret))

def getArticleContent(request):
    try:
        if request.method == 'GET':
            log_error('------')

        ret = return_success()
    except Exception,e:
        log_error('logout with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))

    return HttpResponse(json.dumps(ret))

def modifyArticle(request):
    try:
        log_debug('in addArticle---method:%s' % request.method)
        if not request.session.get('username', None):
            log_error("======user not login")
            ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                     ErrMsg.ERR_MSG_USER_NOT_LOGIN_ERROR))
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

    except Exception,e:
        log_error('login with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))
        log_error("ERR:%s" % ret)
        return HttpResponse(json.dumps(ret))

def deleteArticle(request):
    try:
        log_debug('in addArticle---method:%s' % request.method)
        if not request.session.get('username', None):
            log_error("======user not login")
            ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                     ErrMsg.ERR_MSG_USER_NOT_LOGIN_ERROR))
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

    except Exception,e:
        log_error('login with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))
        log_error("ERR:%s" % ret)
        return HttpResponse(json.dumps(ret))