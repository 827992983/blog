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
            log_debug('request body: %s' % request.body)
            form = json.loads(request.body)

            if form:
                username = form['username']
                password = form['password']

                userinfo = User.objects.filter(username=username)
                if userinfo == None or len(userinfo) != 1:
                    ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                             ErrMsg.ERR_MSG_INTERNAL_ERROR))
                    return HttpResponse(json.dumps(ret))

                db_password = str(userinfo[0].password)
                password = str(password)
                if check_password(password, db_password):
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
            if articleTypes == None:
                ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                         ErrMsg.ERR_MSG_INTERNAL_ERROR))
                return HttpResponse(json.dumps(ret))

            data = []
            for item in articleTypes:
                arcType = {}
                arcType['type_id'] = item.type_id
                arcType['type_name'] = item.type_name
                data.append(arcType)
            ret = return_success(data=data)
        else:
            ret = return_error(Error(ErrCode.ERR_CODE_INVALID_REQUEST_PARAM,
                                     ErrMsg.ERR_MSG_INVALID_REQUEST_PARAM))
    except Exception,e:
        log_error('getArticleType with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))

    return HttpResponse(json.dumps(ret))

def getArticleTitles(request):
    try:
        if request.method == 'GET':
            articleType = request.GET['type_id']
            log_debug('request GET params: type_id:[%s]' % articleType)
            articleTitles = Article.objects.filter(type_id=articleType)
            if articleTitles == None:
                ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                         ErrMsg.ERR_MSG_INTERNAL_ERROR))
                return HttpResponse(json.dumps(ret))

            data = []
            for item in articleTitles:
                arcTitle = {}
                arcTitle['article_id'] = item.article_id
                arcTitle['title'] = item.title
                data.append(arcTitle)
            ret = return_success(data=data)
        else:
            ret = return_error(Error(ErrCode.ERR_CODE_INVALID_REQUEST_PARAM,
                                     ErrMsg.ERR_MSG_INVALID_REQUEST_PARAM))
    except Exception,e:
        log_error('getArticleTitles with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))

    return HttpResponse(json.dumps(ret))

def addArticle(request):
    try:
        if not request.session.get('username', None):
            log_error("user not login")
            ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                     ErrMsg.ERR_MSG_USER_NOT_LOGIN_ERROR))
            return HttpResponse(json.dumps(ret))

        if request.method == 'POST':
            log_debug('request body: %s' % request.body)
            form = json.loads(request.body)

            if form:
                userinfo = User.objects.filter(username=form['author'])
                if userinfo == None or len(userinfo) != 1:
                    ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                             ErrMsg.ERR_MSG_INTERNAL_ERROR))
                    return HttpResponse(json.dumps(ret))
                if userinfo[0].role == const.USER_ROLE_ADMIN:
                    status = const.ATRICLE_STATUS_PUBLISHED
                elif userinfo[0].role == const.USER_ROLE_NORMAL:
                    status = const.ATRICLE_STATUS_PREPARED
                else:
                    ret = return_error(Error(ErrCode.ERR_CODE_INVALID_REQUEST_PARAM,
                                             ErrMsg.ERR_MSG_INVALID_REQUEST_PARAM))
                    return HttpResponse(json.dumps(ret))

                Article.objects.create(article_id = uuid.uuid1(), title = form['title'],
                                       type_id=form['type_id'], author = userinfo[0].real_name,
                                       status=status, html_context = form['html_context'])

                ret = return_success()
                return HttpResponse(json.dumps(ret))
    except Exception,e:
        log_error('addArticle with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))
        return HttpResponse(json.dumps(ret))

def getArticleContent(request):
    try:
        if request.method == 'GET':
            articleID = request.GET['article_id']
            log_debug('request GET params: article_id:[%s]' % articleID)
            article = Article.objects.filter(article_id=articleID)
            if article == None:
                ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                         ErrMsg.ERR_MSG_INTERNAL_ERROR))
                return HttpResponse(json.dumps(ret))

            data = ''
            if len(article) == 1:
                data = article[0].html_context
            ret = return_success(data=data)
        else:
            ret = return_error(Error(ErrCode.ERR_CODE_INVALID_REQUEST_PARAM,
                                     ErrMsg.ERR_MSG_INVALID_REQUEST_PARAM))
    except Exception,e:
        log_error('getArticleContent with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))

    return HttpResponse(json.dumps(ret))

def modifyArticle(request):
    try:
        if not request.session.get('username', None):
            log_error("user not login")
            ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                     ErrMsg.ERR_MSG_USER_NOT_LOGIN_ERROR))
            return HttpResponse(json.dumps(ret))

        if request.method == 'POST':
            log_debug(request.body)
            form = json.loads(request.body)

            if form == None:
                ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                   ErrMsg.ERR_MSG_USER_NOT_LOGIN_ERROR))
                return HttpResponse(json.dumps(ret))

            article_id = form.get('article_id', '')
            html_context = form.get('html_context', '')
            if len(article_id) == 0 or len(html_context) == 0:
                ret = return_error(Error(ErrCode.ERR_CODE_INVALID_REQUEST_PARAM,
                                         ErrMsg.ERR_MSG_INVALID_REQUEST_PARAM))
                return HttpResponse(json.dumps(ret))

            if form.get('operation') == 'modify':
                Article.objects.filter(article_id=article_id).update(html_context=html_context)
            if form.get('operation') == 'delete':
                Article.objects.filter(article_id=article_id).delete()

            ret = return_success()

    except Exception,e:
        log_error('login with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))

    return HttpResponse(json.dumps(ret))
