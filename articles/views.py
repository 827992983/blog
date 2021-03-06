import json
import uuid
from django.shortcuts import render
from django.http import HttpResponse
from admin.models import Article
from admin.models import ArticleComment
from admin.models import ArticleType
from common.logger import log_error,log_info,log_debug
from common.error import return_error, return_success, Error
import common.err_msg as ErrMsg
import common.err_code as ErrCode
import common.constants as const

# Create your views here.

def index(request):
    aritcles = Article.objects.filter()
    if aritcles:
        total = len(aritcles)
    else:
        total = 0

    if total % 5 > 0:
        total = total/5 + 1
    else:
        total = total/5

    if 'page_index' in request.GET:
        index = int(request.GET['page_index'])
    else:
        index = 1

    if index >= total:
        index = total

    if index > 1:
        start = (index-1) * 5
    else:
        index = 1
        start = 0
    end = start + 5

    articlePages = {}
    articlePages['total'] = total if total > 1 else 1
    articlePages['index'] = index if index > 1 else 1

    latest_article_list = Article.objects.filter().order_by("-timestamp")[start:end]
    popular_article_list = Article.objects.filter().order_by("-read_number")[start:end]
    context = {'latest_article_list': latest_article_list,
               'popular_article_list': popular_article_list,}
    articleTypes = ArticleType.objects.filter()
    for item in articleTypes:
        context[item.alias] = {'type_id':item.type_id, 'type_name':item.type_name}
    context['articlePages'] = articlePages
    return render(request, 'static/articles/index.html', context)

def search(request):
    keywords = request.GET['keywords']
    aritcles = Article.objects.filter(title__contains=keywords)
    if aritcles:
        total = len(aritcles)
    else:
        total = 0

    if total % 5 > 0:
        total = total / 5 + 1
    else:
        total = total / 5

    if 'page_index' in request.GET:
        index = int(request.GET['page_index'])
    else:
        index = 1

    if index >= total:
        index = total

    if index > 1:
        start = (index - 1) * 5
    else:
        index = 1
        start = 0

    end = start + 5
    articlePages = {}
    articlePages['total'] = total if total > 1 else 1
    articlePages['index'] = index if index > 1 else 1

    latest_article_list = Article.objects.filter(title__contains=keywords).order_by("-timestamp")[start:end]
    popular_article_list = Article.objects.filter(title__contains=keywords).order_by("-read_number")[start:end]
    context = {'latest_article_list': latest_article_list,
               'popular_article_list': popular_article_list,}
    articleTypes = ArticleType.objects.filter()
    for item in articleTypes:
        context[item.alias] = {'type_id':item.type_id, 'type_name':item.type_name}
    context['articlePages'] = articlePages
    return render(request, 'static/articles/index.html', context)

def indexArticleType(request):
    uri = request.path
    paths = uri.split('/')
    type_id = paths[-1]

    aritcles = Article.objects.filter(type_id=type_id)
    if aritcles:
        total = len(aritcles)
    else:
        total = 0

    if total % 5 > 0:
        total = total / 5 + 1
    else:
        total = total / 5

    if 'page_index' in request.GET:
        index = int(request.GET['page_index'])
    else:
        index = 1

    if index >= total:
        index = total

    if index > 1:
        start = (index - 1) * 5
    else:
        index = 1
        start = 0
    end = start + 5

    articlePages = {}
    articlePages['total'] = total if total > 1 else 1
    articlePages['index'] = index if index > 1 else 1

    latest_article_list = Article.objects.filter(type_id=type_id).order_by("-timestamp")[start:end]
    popular_article_list = Article.objects.filter(type_id=type_id).order_by("-read_number")[start:end]
    context = {'latest_article_list': latest_article_list,
               'popular_article_list': popular_article_list,}
    articleTypes = ArticleType.objects.filter()
    for item in articleTypes:
        context[item.alias] = {'type_id':item.type_id, 'type_name':item.type_name}
    context['articlePages'] = articlePages
    return render(request, 'static/articles/index.html', context)

def article(request):
    try:
        if request.method == 'GET':
            uri = request.path
            paths = uri.split('/')
            article_id = paths[-1]
            #log_debug('request GET URI:[%s], article_id:[%s]' % (uri, article_id))

            articles = Article.objects.filter(article_id=article_id, status=const.ATRICLE_STATUS_PUBLISHED)
            if articles == None:
                ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                         ErrMsg.ERR_MSG_INTERNAL_ERROR))
                return HttpResponse(json.dumps(ret))

            if articles == None or len(articles) != 1:
                ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                         ErrMsg.ERR_MSG_INTERNAL_ERROR))
                return HttpResponse(json.dumps(ret))

            data = {}
            data['article_id'] = articles[0].article_id
            data['title'] = articles[0].title
            data['type_id'] = articles[0].type_id
            data['author'] = articles[0].author
            data['html_context'] = articles[0].html_context
            data['read_number'] = articles[0].read_number
            data['favorite_number'] = articles[0].favorite_number
            data['timestamp'] = articles[0].timestamp

            articleComments = ArticleComment.objects.filter(article_id=article_id)
            data['comment_number'] = len(articleComments)

            ret={'article': data}
            data = []
            for item in articleComments:
                comment = {}
                comment['comment_id'] = item.comment_id
                comment['context'] = item.context
                comment['timestamp'] = item.timestamp
                if item.status == const.ATRICLE_COMMENT_STATUS_VALID:
                    data.append(comment)
            ret['comments'] = data

            articleTypes = ArticleType.objects.filter()
            for item in articleTypes:
                ret[item.alias] = {'type_id': item.type_id, 'type_name': item.type_name}

            return render(request, 'static/articles/article.html', ret)
        else:
            ret = return_error(Error(ErrCode.ERR_CODE_INVALID_REQUEST_PARAM,
                                     ErrMsg.ERR_MSG_INVALID_REQUEST_PARAM))
    except Exception,e:
        log_error('article with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))

    return HttpResponse(json.dumps(ret))

def addComment(request):
    try:
        if request.method == 'POST':
            #log_debug('request body: %s' % request.body)
            form = json.loads(request.body)

            if form:
                articleComments = ArticleComment.objects.filter(article_id=form['article_id'])
                if len(articleComments) > const.LIMIT_ARTICLE_COMMENT_NUMBER:
                    ret = return_error(Error(ErrCode.ERR_CODE_ARTICLE_COMMENT_MAX_NUMBER,
                                             ErrMsg.ERR_MSG_ARTICLE_COMMENT_MAX_NUMBER))
                    return HttpResponse(json.dumps(ret))

                articles = Article.objects.filter(article_id=form['article_id'])
                if articles == None or len(articles) != 1:
                    ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                             ErrMsg.ERR_MSG_INTERNAL_ERROR))
                    return HttpResponse(json.dumps(ret))

                ArticleComment.objects.create(comment_id = uuid.uuid1(), article_id = form['article_id'],
                                              status=const.ATRICLE_COMMENT_STATUS_VALID, context=form['context'])

                ret = return_success()
            else:
                ret = return_error(Error(ErrCode.ERR_CODE_INVALID_REQUEST_PARAM,
                                         ErrMsg.ERR_MSG_INVALID_REQUEST_PARAM))
        else:
            ret = return_error(Error(ErrCode.ERR_CODE_INVALID_REQUEST_PARAM,
                                     ErrMsg.ERR_MSG_INVALID_REQUEST_PARAM))
    except Exception,e:
        log_error('addComment with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))

    return HttpResponse(json.dumps(ret))

def addFavoriteNumber(request):
    try:
        if request.method == 'GET':
            uri = request.path
            paths = uri.split('/')
            article_id = paths[-1]
            #log_debug('request GET URI:[%s], article_id:[%s]' % (uri, article_id))

            articles = Article.objects.filter(article_id=article_id, status=const.ATRICLE_STATUS_PUBLISHED)
            if articles == None:
                ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                         ErrMsg.ERR_MSG_INTERNAL_ERROR))
                return HttpResponse(json.dumps(ret))

            if articles == None or len(articles) != 1:
                ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                         ErrMsg.ERR_MSG_INTERNAL_ERROR))
                return HttpResponse(json.dumps(ret))
            else:
                ret = return_error(Error(ErrCode.ERR_CODE_INVALID_REQUEST_PARAM,
                                         ErrMsg.ERR_MSG_INVALID_REQUEST_PARAM))
            favorite_number = articles[0].favorite_number
            favorite_number = favorite_number + 1
            Article.objects.filter(article_id=article_id).update(favorite_number=favorite_number)
            ret = return_success()
        else:
            ret = return_error(Error(ErrCode.ERR_CODE_INVALID_REQUEST_PARAM,
                                     ErrMsg.ERR_MSG_INVALID_REQUEST_PARAM))
    except Exception,e:
        log_error('addFavoriteNumber with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))

    return HttpResponse(json.dumps(ret))

def addReadNumber(request):
    try:
        if request.method == 'GET':
            uri = request.path
            paths = uri.split('/')
            article_id = paths[-1]
            #log_debug('request GET URI:[%s], article_id:[%s]' % (uri, article_id))

            articles = Article.objects.filter(article_id=article_id, status=const.ATRICLE_STATUS_PUBLISHED)
            if articles == None:
                ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                         ErrMsg.ERR_MSG_INTERNAL_ERROR))
                return HttpResponse(json.dumps(ret))

            if articles == None or len(articles) != 1:
                ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                         ErrMsg.ERR_MSG_INTERNAL_ERROR))
                return HttpResponse(json.dumps(ret))
            else:
                ret = return_error(Error(ErrCode.ERR_CODE_INVALID_REQUEST_PARAM,
                                         ErrMsg.ERR_MSG_INVALID_REQUEST_PARAM))
            read_number = articles[0].read_number
            read_number = read_number + 1
            Article.objects.filter(article_id=article_id).update(read_number=read_number)
            ret = return_success()
        else:
            ret = return_error(Error(ErrCode.ERR_CODE_INVALID_REQUEST_PARAM,
                                     ErrMsg.ERR_MSG_INVALID_REQUEST_PARAM))
    except Exception,e:
        log_error('addReadNumber with Exception:%s' % e)
        ret = return_error(Error(ErrCode.ERR_CODE_INTERNAL_ERROR,
                                 ErrMsg.ERR_MSG_INTERNAL_ERROR))

    return HttpResponse(json.dumps(ret))