#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author:abellee
#date: 2017
#Copyright: free

import os
import django
from common.password import create_hashed_password
from admin.models import User
from admin.models import ArticleType

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

def init_user():
    User.objects.get_or_create(username='abellee',password=create_hashed_password('123456'),real_name='Abel Lee',role='admin')
    User.objects.get_or_create(username='user',password=create_hashed_password('123456'),real_name='user',role='normal')

def init_article_type():
    ArticleType.objects.get_or_create('7eaf413a-8d2b-11e7-bfde-5254d6d221d1', type_name='默认分组', alias='default')
    ArticleType.objects.get_or_create('7eaf413b-8d2b-11e7-bfde-5254d6d221d1', type_name='Python', alias='python')
    ArticleType.objects.get_or_create('7eaf413c-8d2b-11e7-bfde-5254d6d221d1', type_name='C/C++', alias='cpp')
    ArticleType.objects.get_or_create('7eaf413d-8d2b-11e7-bfde-5254d6d221d1', type_name='Java', alias='java')
    ArticleType.objects.get_or_create('7eaf413e-8d2b-11e7-bfde-5254d6d221d1', type_name='前端开发', alias='web')
    ArticleType.objects.get_or_create('7eaf413f-8d2b-11e7-bfde-5254d6d221d1', type_name='数据结构与算法', alias='arithmetic')
    ArticleType.objects.get_or_create('7eaf4140-8d2b-11e7-bfde-5254d6d221d1', type_name='Linux/Windows系统', alias='os')
    ArticleType.objects.get_or_create('7eaf4141-8d2b-11e7-bfde-5254d6d221d1', type_name='OpenStack',alias='openstack')
    ArticleType.objects.get_or_create('7eaf4142-8d2b-11e7-bfde-5254d6d221d1', type_name='Spice VDI', alias='vdi')

#init_user()
#init_article_type()
