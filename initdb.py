#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author:abellee
#date: 2017
#Copyright: free

import os
import django
from common.password import create_hashed_password
import uuid
from admin.models import User
from admin.models import ArticleType

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

def init_user():
    User.objects.get_or_create(username='abellee',password=create_hashed_password('123456'),real_name='Abel Lee',role='admin')
    User.objects.get_or_create(username='user',password=create_hashed_password('123456'),real_name='user',role='normal')

def init_article_type():
    ArticleType.objects.get_or_create(type_id=str(uuid.uuid1()), type_name='默认分组')
    ArticleType.objects.get_or_create(type_id=str(uuid.uuid1()), type_name='python' )
    ArticleType.objects.get_or_create(type_id=str(uuid.uuid1()), type_name='c/c++')
    ArticleType.objects.get_or_create(type_id=str(uuid.uuid1()), type_name='java')
    ArticleType.objects.get_or_create(type_id=str(uuid.uuid1()), type_name='前端开发')
    ArticleType.objects.get_or_create(type_id=str(uuid.uuid1()), type_name='数据结构与算法')
    ArticleType.objects.get_or_create(type_id=str(uuid.uuid1()), type_name='linux/windows系统')
    ArticleType.objects.get_or_create(type_id=str(uuid.uuid1()), type_name='虚拟化云计算')
    ArticleType.objects.get_or_create(type_id=str(uuid.uuid1()), type_name='openstack')
    ArticleType.objects.get_or_create(type_id=str(uuid.uuid1()), type_name='VDI')

#init_user()
init_article_type()
