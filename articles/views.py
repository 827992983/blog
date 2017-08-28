import json
import uuid
from django.shortcuts import render
from django.http import HttpResponse
from admin.models import Article
from admin.models import ArticleComment
from common.logger import log_error,log_info,log_debug
from common.error import return_error, return_success, Error
import common.err_msg as ErrMsg
import common.err_code as ErrCode
import common.constants as const

# Create your views here.

def index(request):
    latest_article_list = Article.objects.filter().order_by("-timestamp")[0:5]
    popular_article_list = Article.objects.filter().order_by("read_number")[0:5]
    context = {'latest_article_list': latest_article_list,
               'popular_article_list': popular_article_list,}
    return render(request, 'static/articles/index.html', context)

def article(request):
    try:
        if request.method == 'GET':
            uri = request.path
            paths = uri.split('/')
            article_id = paths[-1]
            #article_id = request.GET['article_id']
            log_debug('request GET URI:[%s], article_id:[%s]' % (uri, article_id))

            articles = Article.objects.filter(article_id=article_id, status=const.ATRICLE_STATUS_PUBLISHED)
            log_error("=====articles: %s" % articles)
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
            log_error("=====articles:[%s]" % (articleComments))
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

            log_error("=====ret: %s" % ret)
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
        log_error("-----------------------------")
        if request.method == 'POST':
            log_debug('-=-=-=-=request body: %s' % request.body)
            form = json.loads(request.body)

            if form:
                articles = Article.objects.filter(article_id=form['article_id'])
                log_error("-0=0=0=articles:%s" % articles)
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